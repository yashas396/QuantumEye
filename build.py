"""Build script for Render deployment - decompress creditcard.csv.gz if needed."""
import gzip
import os
import shutil

CSV = "creditcard.csv"
GZ = "creditcard.csv.gz"

if not os.path.exists(CSV) and os.path.exists(GZ):
    print(f"Decompressing {GZ} ...")
    with gzip.open(GZ, "rb") as f_in, open(CSV, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    print(f"  {CSV} ready ({os.path.getsize(CSV) / 1024 / 1024:.1f} MB)")
elif os.path.exists(CSV):
    print(f"{CSV} already exists, skipping decompress.")
else:
    print(f"WARNING: neither {CSV} nor {GZ} found!")
