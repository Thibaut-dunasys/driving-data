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

     # dfs = []
     # for f in files:
     #     df = pd.read_csv(f)
     #     df = df[~df["Label"].isin(["Fin", "Initialisation"])]
     #     # df.drop(df.index[-1], inplace=True)
     #     # df.drop(df.index[0], inplace=True)
     #     df["source_file"] = os.path.basename(f)
     #         # 🔹 Format ISO : YYYY-MM-DD HH:MM:SS
     #     df["Start_time"] = df["Start_time"].dt.strftime("%Y-%m-%d %H:%M:%S)
     #     df["End_time"] = df["End_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
     #     dfs.append(df)
         
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df = df[~df["Label"].isin(["Fin", "Initialisation"])]
        df["source_file"] = os.path.basename(f)
        df["Start_time"]=pd.to_datetime(df["Start_time"])
        df["Start_time"]=df["Start_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
         # 1) Parse en datetime (évite aussi le warning dayfirst)
        # df["Start_time"] = pd.to_datetime(df["Start_time"], dayfirst=True, errors="coerce")
        # if "End_time" in df.columns:
        #     df["End_time"] = pd.to_datetime(df["End_time"], dayfirst=True, errors="coerce")
    
         # 2) Format ISO (après conversion)
        # df["Start_time"] = df["Start_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        # if "End_time" in df.columns:
        #     df["End_time"] = df["End_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
        dfs.append(df)


    merged = pd.concat(dfs, ignore_index=True)
    # merged["Start_time"] = pd.to_datetime(merged["Start_time"])
    # merged.sort_values("Start_time", inplace=True)


    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    merged.to_csv(output_file, index=False)
    print(f"✅ Merged {len(files)} files -> {output_file} ({len(merged)} rows)")

if __name__ == "__main__":
    main()
# import glob
# import os
# import sys
# import pandas as pd

# def main():
#     input_glob = sys.argv[1] if len(sys.argv) > 1 else "data/roulage/**/*"
#     output_file = sys.argv[2] if len(sys.argv) > 2 else "data/merged_roulage/all_roulage.csv"

#     candidates = sorted(glob.glob(input_glob, recursive=True))
#     files = [f for f in candidates if f.lower().endswith(".csv")]
#     files = [f for f in files if os.path.normpath(f) != os.path.normpath(output_file)]

#     if not files:
#         print("DEBUG: input_glob =", input_glob)
#         print("DEBUG: found candidates =", len(candidates))
#         print("DEBUG: found csv files =", len(files))
#         print("DEBUG: sample candidates =", candidates[:20])
#         raise SystemExit(f"No CSV files found for glob: {input_glob} (excluding output: {output_file})")

#     dfs = []
#     for f in files:
#         df = pd.read_csv(f)
#         df = df[~df["Label"].isin(["Fin", "Initialisation"])]

#         df["source_file"] = os.path.basename(f)
#         dfs.append(df)

#     merged = pd.concat(dfs, ignore_index=True)

#     # ✅ Parse dates (évite le warning + rend .dt utilisable)
#     # - errors="coerce" => si une date est invalide, elle devient NaT au lieu de faire planter
#     merged["Start_time"] = pd.to_datetime(merged["Start_time"], dayfirst=True, errors="coerce")

#     if "End_time" in merged.columns:
#         merged["End_time"] = pd.to_datetime(merged["End_time"], dayfirst=True, errors="coerce")

#     # ✅ Tri par Start_time
#     merged.sort_values("Start_time", inplace=True)

#     # ✅ Format ISO: YYYY-MM-DD HH:MM:SS (en gardant les NaT -> NaN dans le CSV)
#     merged["Start_time"] = merged["Start_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
#     if "End_time" in merged.columns:
#         merged["End_time"] = merged["End_time"].dt.strftime("%Y-%m-%d %H:%M:%S")

#     out_dir = os.path.dirname(output_file)
#     if out_dir:
#         os.makedirs(out_dir, exist_ok=True)

#     merged.to_csv(output_file, index=False)
#     print(f"✅ Merged {len(files)} files -> {output_file} ({len(merged)} rows)")

# if __name__ == "__main__":
#     main()


