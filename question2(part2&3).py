import os
import pandas as pd
import numpy as np
import glob

def load_temperature_data(data_folder='temperature_data'):
    """
    Load all CSV files from the temperature_data folder into a single DataFrame
    """
    # Get all CSV files from the folder
    csv_files = glob.glob(os.path.join(data_folder, '*.csv'))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in the {data_folder} folder")
    
    # List to store individual dataframes
    dfs = []

    # Read each CSV file
    for file in csv_files:
        df = pd.read_csv(file)
        # Add year information if available from filename
        year = os.path.basename(file).split('_')[-1].split('.')[0]
        if year.isdigit():
            df['YEAR'] = year
        dfs.append(df)

    # Concatenate all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def find_largest_temperature_range_stations (df):
    """
    Find the station(s) with the largest temperature across all years
    """
    # Group by station name to find the largest range for each station
    stations = df['STATION_NAME'].unique()
    station_max_ranges = []

    for station in stations:
        station_data = df[df['STATION_NAME'] == station]

        # For each station, find max and min temperatures across all years
        months = ['January', 'February', 'March', 'April', 'May', 'June','July',
                'August','September', 'October', 'November', 'December']
        all_temps = station_data[months].values.flatten()
        max_temp = np.max(all_temps)
        min_temp = np.min(all_temps)
        temp_range = max_temp - min_temp

        station_max_ranges.append({
            'STATION_NAME': station,
            'MAX_TEMP': max_temp,
            'MIN_TEMP': min_temp,
            'TEMP_RANGE': temp_range
        })
    # convert to DataFrame
    station_ranges_df = pd.DataFrame(station_max_ranges)

    # Find the maximum temperature range
    max_range = station_ranges_df['TEMP_RANGE'].max()

    # Get stations with the maximum range
    largest_range_stations = station_ranges_df[station_ranges_df['TEMP_RANGE'] == max_range][
        ['STATION_NAME', 'MAX_TEMP', 'MIN_TEMP', 'TEMP_RANGE']]

    return largest_range_stations

def find_warmest_and_coolest_stations(df):
    """
    Find the warmest and coolest stations based on annual average temperature
    """
    # Calculate annual average temperature for each station across all years
    stations = df['STATION_NAME'].unique()
    station_avgs =[]
    for station in stations:
        station_data = df[df['STATION_NAME'] == station]
        # Calculate the avarage across all months and years
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August','September', 'October', 'November', 'December']
        avg_temp = np.mean(station_data[months].values.flatten())
        station_avgs.append({
            'STATION_NAME': station,
            'ANNUAL_AVG': avg_temp
        })

    # Convert to DataFrame
    station_avgs_df = pd.DataFrame(station_avgs)
        
    # Find the warmest station(s)
    max_temp = station_avgs_df['ANNUAL_AVG'].max()
    warmest_stations = station_avgs_df[station_avgs_df['ANNUAL_AVG'] == max_temp][['STATION_NAME','ANNUAL_AVG']]

    # Find the coolest station(s)
    min_temp = station_avgs_df['ANNUAL_AVG'].min()
    coolest_stations = station_avgs_df[station_avgs_df['ANNUAL_AVG'] == min_temp][['STATION_NAME','ANNUAL_AVG']]

    return warmest_stations, coolest_stations

def save_results(largest_range_stations, warmest_stations, coolest_stations):
    """
    Save the results to the specified output files
    """
    # Save Largest temperature range stations
    with open('largest_temp_range_stations.txt', 'w') as f:
        f.write("Stations with the largest temperature range:\n")
        for _, row in largest_range_stations.iterrows():
            f.write(f"{row['STATION_NAME']}: {row['TEMP_RANGE']:.2f} °C\n")
            f.write(f"(Max: {row['MAX_TEMP']:.2f} C, Min: {row['MIN_TEMP']:.2f} °C)\n")
    
    # Save warmest and coolest stations
    with open('warmest_and_coolest_station.txt', 'w') as f:
        f.write("Warmest Station: \n")
        for _, row in warmest_stations.iterrows():
            f.write(f"{row['STATION_NAME']}: {row['ANNUAL_AVG']:.2f} °C\n")

        f.write("\nCoolest Stations:\n")
        for _, row in coolest_stations.iterrows():
            f.write(f"{row['STATION_NAME']}: {row['ANNUAL_AVG']:.2f} °C\n")

def main():
    try:
        # Load all temperature data
        data = load_temperature_data()

        # Find stations with largest temperature range
        largest_range = find_largest_temperature_range_stations(data)

        # Find warmest and coolest stations:
        warmest, coolest = find_warmest_and_coolest_stations(data)

        # Save results to files
        save_results(largest_range, warmest, coolest)

        print("Analysis complete. Results saved to output files.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
