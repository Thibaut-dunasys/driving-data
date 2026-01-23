from pathlib import Path
import pandas as pd

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

def main():
    trips = Path("dataV2")
    for csv in trips.rglob("**/*.csv"):
        cleaner = choose_cleaner(csv.name)
        if cleaner is None:
            continue

        df = pd.read_csv(csv)
        df_clean = cleaner(df)

        df_clean.to_csv(csv, index=False)
        print(f"[CLEANED] {csv}")


if __name__ == "__main__":
    main()
