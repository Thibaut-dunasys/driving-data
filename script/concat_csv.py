import glob
import os
import sys
import pandas as pd

def main():
    # Chemins par défaut (TES chemins)
    input_glob = sys.argv[1] if len(sys.argv) > 1 else "data/roulage/*.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/all_roulage/all_roulage.csv"

    # Récupère les CSV et exclut le fichier de sortie s'il matche le glob
    files = sorted(glob.glob(input_glob))
    files = [f for f in files if os.path.normpath(f) != os.path.normpath(output_file)]
    

    if not files:
        raise SystemExit(f"No CSV files found for glob: {input_glob} (excluding output: {output_file})")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df.drop(df.index[-1], inplace=True)
        df.drop(df.index[0], inplace=True)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)

    merged = pd.concat(dfs, ignore_index=True)

    # Crée le dossier de sortie s'il n'existe pas
    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    merged.to_csv(output_file, index=False)
    print(f"✅ Merged {len(files)} files -> {output_file} ({len(merged)} rows)")

if __name__ == "__main__":
    main()
