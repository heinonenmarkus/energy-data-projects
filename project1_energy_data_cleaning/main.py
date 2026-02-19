import pandas as pd


def main():
    #Read csv file
    path = "data/consumption.txt"
    df = pd.read_csv(path)

    # Drop Notes
    df = df.drop(columns=["Notes"], errors="ignore")

    #Date: normalize and parse (fixes 2023/01/10)
    df["Date"] = df["Date"].astype(str).str.strip().str.replace("/", "-", regex=False)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    #Clean Energy_kWh
    df["Energy_kWh"] = (
        df["Energy_kWh"]
        .astype(str)
        .str.strip()
        .replace({"": None, "NA": None, "nan": None, "thirty-five": "35"})
    )
    df["Energy_kWh"] = pd.to_numeric(df["Energy_kWh"], errors="coerce")
    df.loc[df["Energy_kWh"] < 0, "Energy_kWh"] = pd.NA  # negative -> missing

    #Clean Cost_USD
    df["Cost_USD"] = (
        df["Cost_USD"]
        .astype(str)
        .str.strip()
        .replace({"": None, "NA": None, "nan": None, "ten": "10"})
    )
    df["Cost_USD"] = pd.to_numeric(df["Cost_USD"], errors="coerce")

    #Keep only rows with valid Date + Household_ID
    df = df.dropna(subset=["Date", "Household_ID"]).sort_values("Date")

    #Fill missing values
    df = df.set_index("Date").sort_index()
    df["Energy_kWh"] = df["Energy_kWh"].interpolate(method="time").bfill().ffill()
    df["Cost_USD"] = df["Cost_USD"].interpolate(method="time").bfill().ffill()

    #Daily & weekly averages
    daily_avg = df["Energy_kWh"].resample("D").mean()
    weekly_avg = df["Energy_kWh"].resample("W").mean()

    print("Cleaned data (first 10 rows):")
    print(df.head(10))

    print("\nDaily average energy (kWh) (first 10 days):")
    print(daily_avg.head(10))

    print("\nWeekly average energy (kWh) (first 10 weeks):")
    print(weekly_avg.head(10))


if __name__ == "__main__":
    main()
