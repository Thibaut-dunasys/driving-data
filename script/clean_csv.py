from pathlib import Path
import pandas as pd

#----------------LOG-------------------
def get_value_col(df: pd.DataFrame) -> str:
    # Priorité: capability, value, puis "la seule colonne non-Time"
    for c in ["capability", "value", "Value"]:
        if c in df.columns:
            return c
    non_time = [c for c in df.columns if c.lower() not in ("time", "timestamp", "date")]
    if len(non_time) == 1:
        return non_time[0]
    raise ValueError(f"Impossible d'identifier la colonne valeur. Colonnes={list(df.columns)}")


# ---------- CLEANERS ----------

def clean_odometer(df):
    if "capability" in df.columns:
        df = df.rename(columns={"capability": "DistanceTotalizer(km)"})

    col = "DistanceTotalizer(km)"
    df[col] = (
        df[col].astype(str)
        .str.replace("km", "", regex=False)
        .str.replace("rpm", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce").round().astype("Int64")
    return df


def clean_speed(df):
    if "capability" in df.columns:
        df = df.rename(columns={"capability": "Speed(km/h)"})

    col = "Speed(km/h)"
    df[col] = (
        df[col].astype(str)
        .str.replace("km/h", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce").round().astype("Int64")
    return df


def clean_engine_speed(df):
    if "capability" in df.columns:
        df = df.rename(columns={"capability": "rpm"})

    df["rpm"] = (
        df["rpm"].astype(str)
        .str.replace("rpm", "", regex=False)
        .str.strip()
    )
    df["rpm"] = pd.to_numeric(df["rpm"], errors="coerce").round().astype("Int64")
    return df


# ---------- DISPATCH ----------

def choose_cleaner(filename):
    f = filename.lower()
    if "engine_speed" in f:
        return clean_engine_speed
    if "speed" in f:
        return clean_speed
    if "mileage" in f or "milleage" in f:
        return clean_odometer
    return None


# ---------- MAIN ----------

# def main():
#     from pathlib import Path

def main():
    root = Path("dataV2")
    files = sorted(root.rglob("**/*.csv"))
    print(f"CSV trouvés: {len(files)}")
    for p in files[:200]:  # limite à 200 pour pas spam
        print(p.as_posix())

    # root = Path("dataV2")
    # n_csv = 0
    # n_matched = 0
    # n_changed = 0

    # for csv in root.rglob("*.csv"):
    #     n_csv += 1
    #     cleaner = choose_cleaner(csv.name)
    #     if cleaner is None:
    #         continue

    #     n_matched += 1
    #     df = pd.read_csv(csv)

    #     # Debug colonnes
    #     print(f"\n[MATCH] {csv} | cols={list(df.columns)}")

    #     # Snapshot avant/après (sur la colonne valeur)
    #     val_col = get_value_col(df)
    #     before = df[val_col].astype(str).head(5).tolist()

    #     df_clean = cleaner(df)

    #     after_col = get_value_col(df_clean)
    #     after = df_clean[after_col].astype(str).head(5).tolist()

    #     # Détecter un vrai changement
    #     if before != after or df_clean.shape != df.shape or list(df_clean.columns) != list(df.columns):
    #         n_changed += 1
    #         df_clean.to_csv(csv, index=False)
    #         print(f"[CHANGED] wrote file. sample before={before} after={after}")
    #     else:
    #         print(f"[UNCHANGED] sample before={before} after={after}")

    # print(f"\nRésumé: scanned={n_csv} matched={n_matched} changed={n_changed}")
    # trips = Path("dataV2")
    # for csv in trips.rglob("**/*.csv"):
    #     cleaner = choose_cleaner(csv.name)
    #     if cleaner is None:
    #         continue

    #     df = pd.read_csv(csv)
    #     df_clean = cleaner(df)

    #     df_clean.to_csv(csv, index=False)
    #     print(f"[CLEANED] {csv}")


if __name__ == "__main__":
    main()


