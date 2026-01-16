import glob
import os
import pandas as pd

IN_DIR = "data/incoming"
OUT_FILE = "data/merged/all.csv"

files = sorted(glob.glob(os.path.join(IN_DIR, "*.csv")))
if not files:
    raise SystemExit("No CSV files found.")

dfs = []
for f in files:
    df = pd.read_csv(f)
    df["source_file"] = os.path.basename(f)
    dfs.append(df)

merged = pd.concat(dfs, ignore_index=True)

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
merged.to_csv(OUT_FILE, index=False)
print(f"Wrote {OUT_FILE} with {len(merged)} rows from {len(files)} files.")
