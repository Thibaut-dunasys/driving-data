import glob
import os
import sys
import pandas as pd

def main():
    # Arguments depuis GitHub Actions (ou valeurs par défaut)
    input_glob = sys.argv[1] if len(sys.argv) > 1 else "data/roulage/*.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/all_roulage/all.csv"

    # Liste des fichiers à concaténer
    files = sorted(glob.glob(input_glob))
    if not files:
        raise SystemExit(f"No CSV files found for glob: {input_glob}")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)

    merged = pd.concat(dfs, ignore_index=True)

    # 🔴 POINT CLÉ : créer le dossier de sortie s’il n’existe pas
    output_dir = os.path.dirname(output_file)
    if output_dir:  # évite erreur si fichier à la racine
        os.makedirs(output_dir, exist_ok=True)

    # Écriture du fichier final
    merged.to_csv(output_file, index=False)

    print(f"✅ Merged {len(files)} files -> {output_file} ({len(merged)} rows)")

if __name__ == "__main__":
    main()
