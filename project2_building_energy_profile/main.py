import pandas as pd
import matplotlib.pyplot as plt

def main():

    #Reading the file
    df = pd.read_csv(
        "data/household_power_consumption.txt",
        sep=";",
        na_values="?",
        low_memory=False
    )

    #Combine date and time to datetime
    df["Timestamp"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        dayfirst=True,
        errors="coerce"
    )

    #Convert energy usage to numeric
    df["Global_active_power"] = pd.to_numeric(df["Global_active_power"], errors="coerce")

    #Index data by time and drop missing rows
    df = df.dropna(subset=["Timestamp", "Global_active_power"])
    df = df.set_index("Timestamp").sort_index()

    #Resample data into hourly data
    hourly = df["Global_active_power"].resample("h").mean()

    #Create hourly profile
    hourly_profile = hourly.groupby(hourly.index.hour).mean()

    #Recognize peak hours
    peak_hours = hourly_profile.sort_values(ascending=False).head(5)
    print(peak_hours)

    #Weekend vs Weekday usage
    weekday_avg = hourly[hourly.index.dayofweek < 5].mean()
    weekend_avg = hourly[hourly.index.dayofweek >= 5].mean()

    print("Weekday average:", weekday_avg)
    print("Weekend average:", weekend_avg)

    #Plot the results
    ax = hourly_profile.plot()
    ax.set_xlabel("Hour of day (0–23)")
    ax.set_title("Average Hourly Load Profile")
    ax.set_ylabel("Global active power (kW)")

    plt.show()

if __name__ == "__main__":
        main()