# Import all Python libraries
import csv
import os

# Folder containing data
directory = "./temperature_data"
temperature_data = []

# Month list
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Read CSV file in directory
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        with open(file_path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temps = {}
                for month in months:
                    if month in row and row[month].strip() != "":
                        try:
                            temps[month] = float(row[month])
                        except ValueError:
                            continue
                if "STATION_NAME" in row:
                    station_name = row["STATION_NAME"]
                    station_data = {
                        "Station_Name": station_name,
                        "Temperatures": temps
                    }
                    temperature_data.append(station_data)


def avg():
    seasons = {
        "Spring": ["September", "October", "November"],
        "Summer": ["December", "January", "February"],
        "Autumn": ["March", "April", "May"],
        "Winter": ["June", "July", "August"]
    }

    seasons_data = {season: {"sum": 0, "count": 0} for season in seasons}

    for station in temperature_data:
        temperatures = station["Temperatures"]
        for season, months_in_season in seasons.items():
            for month in months_in_season:
                if month in temperatures:
                    seasons_data[season]["sum"] += temperatures[month]
                    seasons_data[season]["count"] += 1

    # Calculate averages for each season
    averages = {}
    for season, data in seasons_data.items():
        if data["count"] > 0:
            averages[season] = data["sum"] / data["count"]
        else:
            averages[season] = 0

    # Results to text file
    with open("average_temp.txt", "w") as f:
        for season, avg_temp in averages.items():
            f.write(f"{season}: {avg_temp:.2f}°C\n")

    print("Average temperatures saved to 'average_temp.txt'")
    print(averages)

# Call the avg function
if __name__ == "__main__":
    avg()
