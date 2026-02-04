"""
Build script for Render deployment.
1. Decompress creditcard.csv.gz if needed
2. Preprocess data (subsample, fit scaler/PCA, build stream queue)
3. Save preprocessed files so the app never loads the full CSV at runtime
"""
import gzip
import os
import pickle
import shutil

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

CSV = "creditcard.csv"
GZ = "creditcard.csv.gz"
PREPROCESS_DIR = "preprocessed"
PCA_COMPONENTS = 4

# ── Step 1: Decompress CSV ──
if not os.path.exists(CSV) and os.path.exists(GZ):
    print(f"Decompressing {GZ} ...")
    with gzip.open(GZ, "rb") as f_in, open(CSV, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"  {CSV} ready ({os.path.getsize(CSV) / 1024 / 1024:.1f} MB)")
elif os.path.exists(CSV):
    print(f"{CSV} already exists, skipping decompress.")
else:
    print(f"WARNING: neither {CSV} nor {GZ} found!")
    exit(0)

# ── Step 2: Preprocess ──
print("\n[Preprocess] Loading CSV...")
df = pd.read_csv(CSV)
print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
total_rows = len(df)

normal_df = df[df["Class"] == 0]
fraud_df = df[df["Class"] == 1]

# Subsample: 1000 normal + all 492 fraud (matches training notebook)
normal_sample = normal_df.sample(n=1000, random_state=42)
df_small = pd.concat([normal_sample, fraud_df]).reset_index(drop=True)

feature_cols = list(df_small.columns[:-1])  # everything except 'Class'
print(f"  Features ({len(feature_cols)}): {feature_cols[:3]}...{feature_cols[-2:]}")

# MinMaxScaler (-1, 1)
scaler = MinMaxScaler(feature_range=(-1, 1))
df_small[feature_cols] = scaler.fit_transform(df_small[feature_cols])

# PCA to 4 components
pca = PCA(n_components=PCA_COMPONENTS)
df_pca = pd.DataFrame(
    pca.fit_transform(df_small[feature_cols]),
    columns=[f"PC{i+1}" for i in range(PCA_COMPONENTS)]
)
df_pca["Class"] = df_small["Class"].values
print(f"  PCA variance ratio: {pca.explained_variance_ratio_.round(4).tolist()}")

# Train/test split
train_normal, val_normal = train_test_split(
    df_pca[df_pca["Class"] == 0], test_size=0.2, random_state=42
)
X_train = train_normal.drop("Class", axis=1).values.astype(np.float32)
test_mixed = pd.concat([val_normal, df_pca[df_pca["Class"] == 1]])
X_test = test_mixed.drop("Class", axis=1).values.astype(np.float32)
y_test = test_mixed["Class"].values

print(f"  Train (normal): {X_train.shape}")
print(f"  Test (mixed):   {X_test.shape} ({sum(y_test==0)} normal, {sum(y_test==1)} fraud)")

# Build stream queue (shuffled mix from full dataset)
stream_normal = normal_df.sample(n=min(2000, len(normal_df)), random_state=123)
stream_combined = pd.concat([stream_normal, fraud_df]).sample(frac=1, random_state=42)
stream_queue = stream_combined.to_dict("records")
print(f"  Stream queue: {len(stream_queue)} transactions")

# ── Step 3: Save preprocessed files ──
os.makedirs(PREPROCESS_DIR, exist_ok=True)

with open(os.path.join(PREPROCESS_DIR, "pipeline.pkl"), "wb") as f:
    pickle.dump({
        "scaler": scaler,
        "pca": pca,
        "feature_cols": feature_cols,
        "X_train": X_train,
        "X_test": X_test,
        "y_test": y_test,
        "stream_queue": stream_queue,
        "total_rows": total_rows,
    }, f)

size_mb = os.path.getsize(os.path.join(PREPROCESS_DIR, "pipeline.pkl")) / 1024 / 1024
print(f"\n[Preprocess] Saved preprocessed data ({size_mb:.1f} MB)")

# ── Step 4: Convert model weights from torch to numpy ──
print("\n[Model] Converting torch weights to numpy...")
import torch
import warnings

MODEL_DIR = "qdt_fraud_model"
pkl_path = os.path.join(MODEL_DIR, "data.pkl")

class _Loader(pickle.Unpickler):
    def persistent_load(self, saved_id):
        _tag, _cls, key, _loc, numel = saved_id
        fpath = os.path.join(MODEL_DIR, "data", str(key))
        nbytes = int(numel) * 4
        storage = torch.UntypedStorage.from_file(fpath, shared=False, nbytes=nbytes)
        return torch.storage.TypedStorage(wrap_storage=storage, dtype=torch.float32)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with open(pkl_path, "rb") as f:
        sd = _Loader(f).load()

weights_np = {}
for k, v in sd.items():
    if isinstance(v, torch.Tensor):
        weights_np[k] = v.numpy()
        print(f"  {k}: {v.shape}")

np.savez(os.path.join(PREPROCESS_DIR, "model_weights.npz"), **weights_np)
size_mb2 = os.path.getsize(os.path.join(PREPROCESS_DIR, "model_weights.npz")) / 1024 / 1024
print(f"  Saved model weights as numpy ({size_mb2:.2f} MB)")

print("\n[Build] Done. No torch or pandas needed at runtime.")
