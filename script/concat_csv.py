import glob
import os
import sys
import pandas as pd

def main():
    input_glob = sys.argv[1] if len(sys.argv) > 1 else "data/roulage/**/*"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/merged_roulage/all_roulage.csv"

    # Cherche récursivement, puis garde uniquement les .csv (insensible à la casse)
    candidates = sorted(glob.glob(input_glob, recursive=True))
    files = [f for f in candidates if f.lower().endswith(".csv")]

    # Exclut le fichier merged (au cas où)
    files = [f for f in files if os.path.normpath(f) != os.path.normpath(output_file)]

    if not files:
        # Debug utile dans les logs GitHub Actions
        print("DEBUG: input_glob =", input_glob)
        print("DEBUG: found candidates =", len(candidates))
        print("DEBUG: found csv files =", len(files))
        print("DEBUG: sample candidates =", candidates[:20])
        raise SystemExit(f"No CSV files found for glob: {input_glob} (excluding output: {output_file})")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df = df[~df["Label"].isin(["Fin", "Initialisation"])]
        # df.drop(df.index[-1], inplace=True)
        # df.drop(df.index[0], inplace=True)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)

    merged = pd.concat(dfs, ignore_index=True)

    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    merged.to_csv(output_file, index=False)
    print(f"✅ Merged {len(files)} files -> {output_file} ({len(merged)} rows)")

if __name__ == "__main__":
    main()

