import os
import pandas as pd
import numpy as np
import glob

# Define months
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

# Define the months for each season
SEASONS = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

def load_temperature_data(data_folder='temperature_data'):
    """
    Load all CSV files from the temperature_data folder into a single DataFrame.
    Adds a 'YEAR' column extracted from the filename.
    """
    # Get list of all CSV files in the folder
    csv_files = glob.glob(os.path.join(data_folder, '*.csv'))

    # If no files are found, raise an error
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in the {data_folder} folder")

    # List to store individual dataframes
    dfs = []

    # Read each CSV file
    for file in csv_files:
        df = pd.read_csv(file)

        # Extract year from filename and add it as a column
        year = os.path.basename(file).split('_')[-1].split('.')[0]
        if year.isdigit():
            df['YEAR'] = year
        dfs.append(df)

    # Combine all individual DataFrames into one
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def calculate_seasonal_averages(df):
    """
    Calculate the average temperature for each season across all stations and years.
    """
    seasonal_averages = {}
    for season, months in SEASONS.items():
        # Flatten the values from the selected seasonal months
        season_data = df[months].values.flatten()
        # Compute the average temperature for the season
        seasonal_averages[season] = np.mean(season_data)

    return seasonal_averages

def find_largest_temperature_range_stations(df):
    """
    Find station(s) with the largest temperature range (max - min) across all years.
    """
    station_max_ranges = []

    # Loop through each unique station
    for station in df['STATION_NAME'].unique():
        # Filter data for this station
        station_data = df[df['STATION_NAME'] == station]

        # Get all monthly temperatures for this station
        all_temps = station_data[MONTHS].values.flatten()

        # Calculate max and min temperature, then the range
        max_temp = np.max(all_temps)
        min_temp = np.min(all_temps)
        temp_range = max_temp - min_temp

        # Store the results
        station_max_ranges.append({
            'STATION_NAME': station,
            'MAX_TEMP': max_temp,
            'MIN_TEMP': min_temp,
            'TEMP_RANGE': temp_range
        })

    # Create a DataFrame of station temperature ranges
    station_ranges_df = pd.DataFrame(station_max_ranges)

    # Find the maximum temperature range
    max_range = station_ranges_df['TEMP_RANGE'].max()

    # Filter and return only stations with the maximum range
    largest_range_stations = station_ranges_df[station_ranges_df['TEMP_RANGE'] == max_range][
        ['STATION_NAME', 'MAX_TEMP', 'MIN_TEMP', 'TEMP_RANGE']]

    return largest_range_stations

def find_warmest_and_coolest_stations(df):
    """
    Find the warmest and coolest stations based on their annual average temperature.
    """
    station_avgs = []

    # Loop through each station
    for station in df['STATION_NAME'].unique():
        # Filter data for the station
        station_data = df[df['STATION_NAME'] == station]

        # Calculate the average of all 12 months
        avg_temp = np.mean(station_data[MONTHS].values.flatten())

        # Store station and its average temperature
        station_avgs.append({
            'STATION_NAME': station,
            'ANNUAL_AVG': avg_temp
        })

    # Create DataFrame of annual averages
    station_avgs_df = pd.DataFrame(station_avgs)

    # Find the highest and lowest average temperatures
    max_temp = station_avgs_df['ANNUAL_AVG'].max()
    min_temp = station_avgs_df['ANNUAL_AVG'].min()

    # Get stations with max and min averages
    warmest_stations = station_avgs_df[station_avgs_df['ANNUAL_AVG'] == max_temp]
    coolest_stations = station_avgs_df[station_avgs_df['ANNUAL_AVG'] == min_temp]

    return warmest_stations, coolest_stations

def save_results(seasonal_averages, largest_range_stations, warmest_stations, coolest_stations):
    """
    Save the results to the specified output files
    """

    # Write seasonal averages to a file
    with open('average_temp.txt', 'w') as f:
        f.write("Average Temperature for Each Season:\n")
        for season, avg in seasonal_averages.items():
            f.write(f"{season}: {avg:.2f} °C\n")

    # Write largest temperature range station(s) to a file
    with open('largest_temp_range_stations.txt', 'w') as f:
        f.write("Stations with the largest temperature range:\n")
        for _, row in largest_range_stations.iterrows():
            f.write(f"{row['STATION_NAME']}: {row['TEMP_RANGE']:.2f} °C\n")
            f.write(f"(Max: {row['MAX_TEMP']:.2f} °C, Min: {row['MIN_TEMP']:.2f} °C)\n")

    # Write warmest and coolest stations to a file
    with open('warmest_and_coolest_station.txt', 'w') as f:
        f.write("Warmest Station(s):\n")
        for _, row in warmest_stations.iterrows():
            f.write(f"{row['STATION_NAME']}: {row['ANNUAL_AVG']:.2f} °C\n")

        f.write("\nCoolest Station(s):\n")
        for _, row in coolest_stations.iterrows():
            f.write(f"{row['STATION_NAME']}: {row['ANNUAL_AVG']:.2f} °C\n")

def main():
    """
    Main execution function to run the full analysis.
    """
    try:
        # Load data from CSV files
        data = load_temperature_data()

        # Compute seasonal averages
        seasonal_avgs = calculate_seasonal_averages(data)

        # Find station(s) with the largest temperature range
        largest_range = find_largest_temperature_range_stations(data)

        # Find warmest and coolest stations
        warmest, coolest = find_warmest_and_coolest_stations(data)

        # Save all results to files
        save_results(seasonal_avgs, largest_range, warmest, coolest)

        print("Analysis complete. Results saved to output files.")
    except Exception as e:
        # Catch and print any errors during execution
        print(f"Error: {e}")

# Run the program
if __name__ == "__main__":
    main()
