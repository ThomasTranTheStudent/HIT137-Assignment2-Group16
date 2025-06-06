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

def find_largest_temperature_range_station(df):
    """
    Find the station and year with the largest temperature range (max - min)
    based on each station's data for each individual year.
    """
    station_max_ranges = []

    # Loop through each unique station
    for station in df['STATION_NAME'].unique():
        station_data = df[df['STATION_NAME'] == station]

        # Loop through each year for that station
        for year in station_data['YEAR'].unique():
            year_data = station_data[station_data['YEAR'] == year]

            # Get all temperatures for that year (flatten to handle any multi-row case)
            all_temps = year_data[MONTHS].values.flatten()
            all_temps = all_temps[~np.isnan(all_temps)]  # Remove NaNs if any

            if len(all_temps) == 0:
                continue  # Skip empty data

            # Calculate max and min temperature, then the range
            max_temp = np.max(all_temps)
            min_temp = np.min(all_temps)
            temp_range = max_temp - min_temp

            # Store the results
            station_max_ranges.append({
                'STATION_NAME': station,
                'YEAR': year,
                'MAX_TEMP': max_temp,
                'MIN_TEMP': min_temp,
                'TEMP_RANGE': temp_range
            })

    # Create a DataFrame of station temperature ranges
    station_ranges_df = pd.DataFrame(station_max_ranges)

    # Find the maximum temperature range
    max_range = station_ranges_df['TEMP_RANGE'].max()

    # Filter and return only stations with the maximum range
    largest_range_station = station_ranges_df[station_ranges_df['TEMP_RANGE'] == max_range][
        ['STATION_NAME', 'YEAR', 'MAX_TEMP', 'MIN_TEMP', 'TEMP_RANGE']]

    return largest_range_station

def find_warmest_and_coolest_stations(df):
    """
    Find the warmest and coolest stations by comparing their annual average temperature.
    """
    station_avgs = []

    # Loop through each station
    for station in df['STATION_NAME'].unique():
        station_data = df[df['STATION_NAME'] == station]

        for year in station_data['YEAR'].unique():
            year_data = station_data[station_data['YEAR'] == year]

            # Flatten all monthly values and ignore NaNs
            temps = year_data[MONTHS].values.flatten()
            temps = temps[~np.isnan(temps)]

            if len(temps) == 0:
                continue  # Skip if no temperature data for this year

            avg_temp = np.mean(temps)

            #Store the results
            station_avgs.append({
                'STATION_NAME': station,
                'YEAR': year,
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

    # Write largest temperature range station to a file
    with open('largest_temp_range_station.txt', 'w') as f:
        f.write("Station with the largest temperature range:\n")
        for _, row in largest_range_stations.iterrows():
            f.write(f"{row['STATION_NAME']} ({row['YEAR']}): {row['TEMP_RANGE']:.2f} °C\n")
            f.write(f"(Max: {row['MAX_TEMP']:.2f} °C, Min: {row['MIN_TEMP']:.2f} °C)\n")

    # Write warmest and coolest stations to a file
    with open('warmest_and_coolest_station.txt', 'w') as f:
        f.write("Warmest Station(s):\n")
        for _, row in warmest_stations.iterrows():
            f.write(f"{row['STATION_NAME']} ({row['YEAR']}): {row['ANNUAL_AVG']:.2f} °C\n")

        f.write("\nCoolest Station(s):\n")
        for _, row in coolest_stations.iterrows():
            f.write(f"{row['STATION_NAME']} ({row['YEAR']}): {row['ANNUAL_AVG']:.2f} °C\n")

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
        largest_range = find_largest_temperature_range_station(data)

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
