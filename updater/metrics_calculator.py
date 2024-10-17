import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from datetime import timedelta
from sklearn.linear_model import LinearRegression



def parse_locations(filepath):
    # Parse the locations file to extract spot names, descriptions, and coordinates
    locations = {}
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if ',' in line and "#" not in line:  # To avoid empty lines or malformed lines
                parts = line.split(',')
                spot_name = parts[0].strip()  # Extract the spot name
                description = parts[1].strip()  # Extract the description
                lat = float(parts[2].strip())  # Extract the latitude
                lon = float(parts[3].strip())  # Extract the longitude
                locations[spot_name] = {'coords': (lat, lon), 'description': description}
    return locations

def plot_spots_with_map(data_dict, datetimes, locations_filepath, margin=2):
    # Step 1: Parse the locations file
    locations = parse_locations(locations_filepath)

    # Step 2: Filter spots that are in the locations file
    filtered_spots = {spot: data_dict[spot] for spot in locations if spot in data_dict}
    sorted_spots = sorted(filtered_spots.keys(), key=lambda x: max(filtered_spots[x]), reverse=True)

    # Step 3: Assign colors for each spot using a colormap
    colormap = plt.get_cmap('tab10', len(sorted_spots))  # You can use any other colormap
    spot_colors = {spot: colormap(i) for i, spot in enumerate(sorted_spots)}

    # Step 4: Create a GeoDataFrame for the coordinates
    geometry = [Point(locations[spot]['coords'][1], locations[spot]['coords'][0]) for spot in sorted_spots]
    gdf = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")  # Coordinate system WGS84

    # Reproject to Web Mercator (EPSG:3857) for proper plotting on contextily map
    gdf = gdf.to_crs(epsg=3857)

    # Calculate the extent (bounding box) of all the spots
    minx, miny, maxx, maxy = gdf.total_bounds

    # Add a margin to the bounding box to include surrounding area
    x_margin = (maxx - minx) * margin
    y_margin = (maxy - miny) * margin

    # Set the extent of the map to include the margin
    map_extent = [minx - x_margin, maxx + x_margin, miny - y_margin, maxy + y_margin]

    # Plot 6 spots at a time with the crowd data and the map side by side
    for i in range(0, len(sorted_spots), 6):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))  # Two subplots, side by side

        # Select the next 6 spots to plot
        current_spots = sorted_spots[i:i+6]

        # Plot the crowd data in the first subplot with the assigned color
        for spot in current_spots:
            color = spot_colors[spot]
            description = locations[spot]['description']
            label = f"{spot} ({description})"  # Spot name and description in the legend
            ax1.plot(datetimes, data_dict[spot], label=label, color=color)

        # Customize the crowd plot
        ax1.set_title(f'Spot Crowds from {i+1} to {i+len(current_spots)}')
        ax1.set_xlabel('Datetime')
        ax1.set_ylabel('Crowd Size')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        # Plot the map of the spots in the second subplot
        gdf_subset = gdf.iloc[i:i+6]  # Subset of the current spots' locations

        # Plot the dots with the same color as the crowd data
        for j, spot in enumerate(current_spots):
            color = spot_colors[spot]
            gdf_subset.iloc[[j]].plot(ax=ax2, color=[color], markersize=50, alpha=0.7)

            # Annotate with the spot's description
            ax2.annotate(locations[spot]['description'],
                         (gdf_subset.geometry.iloc[j].x, gdf_subset.geometry.iloc[j].y),
                         xytext=(3, 3), textcoords='offset points', fontsize=8, color='black')

        # Set map bounds with surrounding area
        ax2.set_xlim(map_extent[0], map_extent[1])
        ax2.set_ylim(map_extent[2], map_extent[3])

        # Add basemap (OpenStreetMap)
        ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik)

        # Customize the map
        ax2.set_title(f'Locations of Spots from {i+1} to {i+len(current_spots)}')

        # Show both plots in the same figure
        plt.show()

def plot_spots(data_dict, datetimes):
    # Step 1: Sort spots by max crowd observed, ignoring None values
    def safe_max(crowd_list):
        cleaned_list = [x for x in crowd_list if x is not None]
        return max(cleaned_list) if cleaned_list else 0  # Return 0 if all values are None

    sorted_spots = sorted(data_dict.keys(), key=lambda x: safe_max(data_dict[x]), reverse=True)

    # Print the sorted spot names
    print("Total APs: " + str(len(list(data_dict.keys()))))
    print("APs sorted by max crowd size:")
    for i, spot in enumerate(sorted_spots):
        print(i, spot)

    # Step 2: Function to plot 6 spots at a time
    for i in range(0, len(sorted_spots), 6):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Select the next 6 spots to plot (or fewer if at the end)
        current_spots = sorted_spots[i:i + 6]

        # Plot each spot in current_spots
        for spot in current_spots:
            ax.plot(datetimes, data_dict[spot], label=spot)

        # Customize the plot
        ax.set_title(f'Spot Crowds from {i + 1} to {i + len(current_spots)}')
        ax.set_xlabel('Datetime')
        ax.set_ylabel('Crowd Size')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot and wait until it's closed
        plt.show()

class Measurement:
    def __init__(self, datetime, json_data):
        self.datetime = datetime
        try:
            self.json_data = json.loads(json_data)
        except json.JSONDecodeError:
            self.json_data = None
            print(f"Failed to decode JSON: {json_data}")

    def __repr__(self):
        return f"Measurement(datetime={self.datetime}, json_data={str(self.json_data)})"

def perform_analysis(measurement):
    ap_dict = defaultdict(int)
    for entry in measurement.json_data["4"]["value"]:
        if "empty_cell" in str(entry):
            continue
        ap_dict[str(entry)] += 1
    return ap_dict

def get_data(hours=6):
    try:
        # Fetch database connection details from environment variables
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            cursor = connection.cursor()

            # First, find the most recent entry's timestamp
            cursor.execute("SELECT MAX(recvTimeTs) FROM WLC_LESXI_WLCdata")
            last_entry_timestamp = float(cursor.fetchone()[0])
            last_entry_datetime = datetime.fromtimestamp(last_entry_timestamp / 1000.0)  # Assuming timestamp is in milliseconds

            # Calculate 6 hours before the last entry
            start_time = last_entry_datetime - timedelta(hours=hours)

            # Query to fetch all entries from the last 5 hours from the most recent entry
            cursor.execute("""
                SELECT attrName, attrValue, recvTimeTs
                FROM WLC_LESXI_WLCdata 
                WHERE recvTimeTs BETWEEN %s AND %s 
                ORDER BY recvTimeTs DESC
            """, (
                int(start_time.timestamp() * 1000),  # Start of the 6-hour window
                int(last_entry_datetime.timestamp() * 1000)  # Timestamp of the last entry
            ))

            results = cursor.fetchall()
            measurements = []
            paired_entries = {}

            # Group entries by recvTimeTs
            for name, value, recv_time_ts in results:
                if recv_time_ts not in paired_entries:
                    paired_entries[recv_time_ts] = {}
                if name == 'DateTime':
                    paired_entries[recv_time_ts]['datetime'] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                elif name == 'csvData':
                    paired_entries[recv_time_ts]['json_data'] = value

            # Create Measurement objects from paired entries
            for entry in paired_entries.values():
                if 'datetime' in entry and 'json_data' in entry:
                    measurements.append(Measurement(entry['datetime'], entry['json_data']))
                else:
                    print("Problem, missing corresponding attributes")

            print(f"Total combined entries: {len(measurements)}")

            aps_snapshots = []
            aps_datetimes = []
            aps_names = set()



            #CLEANING
            measurements_clean=[]
            for measurement in measurements:
                if "2" in list(measurement.json_data.keys()) and "4" in list(measurement.json_data.keys()):
                    measurements_clean.append(measurement)
            measurements=measurements_clean
            #

            for measurement in measurements:
                for key in perform_analysis(measurement):
                    aps_names.add(key)

            for measurement in measurements:
                result = perform_analysis(measurement)
                for key in aps_names:
                    if key not in result:
                        result[key] = 0
                aps_snapshots.append(result)
                aps_datetimes.append(measurement.datetime)

            aps_history = defaultdict(list)
            for status in aps_snapshots:
                for ap in status:
                    aps_history[ap].append(status[ap])

            return sort_by_time(aps_datetimes, aps_history)
            return aps_history,aps_datetimes
    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def sort_by_time(aps_datetimes, aps_history):
    # Ensure the dictionary and datetime list are sorted according to the datetime list
    # First, pair each datetime with its index for sorting
    indexed_datetimes = list(enumerate(aps_datetimes))
    # Sort the indexed datetime list by datetime values
    indexed_datetimes.sort(key=lambda x: x[1])

    # Create a new sorted list of datetimes
    sorted_datetimes = [aps_datetimes[index] for index, _ in indexed_datetimes]

    # Create a new dictionary where each list of device entries is sorted to match the sorted datetime list
    sorted_aps_history = defaultdict(list)
    for key in aps_history:
        # Reorder each list in the dictionary according to the new datetime order
        sorted_list = [aps_history[key][index] for index, _ in indexed_datetimes]
        sorted_aps_history[key] = sorted_list

    return  sorted_aps_history,sorted_datetimes

def moving_average(data, window_size):
    """Applies a moving average filter to smooth the data."""
    cumulative_sum = np.cumsum(np.insert(data, 0, 0)) 
    smoothed_data = (cumulative_sum[window_size:] - cumulative_sum[:-window_size]) / window_size
    return smoothed_data

def get_last_week_predictions(aps_history, aps_datetimes, special_ap, additional_aps, group_2, combined_group_1, combined_group_2, smoothing_window=10):
    # Fetch data for the last 7 days (to cover last week)
    aps_history_7d, aps_datetimes_7d = get_data(hours=168)  # 168 hours = 7 days

    # Define the time range for prediction: same 2-hour period from last week
    last_timestamp = aps_datetimes[-1]
    start_prediction_time = last_timestamp - timedelta(days=7)  # Fetch data exactly one week ago
    end_prediction_time = start_prediction_time + timedelta(hours=2)  # 2-hour period

    # Find the indices for the last week's relevant time frame
    last_week_indices = [i for i, dt in enumerate(aps_datetimes_7d) if start_prediction_time <= dt <= end_prediction_time]

    # Initialize lists for last week's prediction data
    predicted_group_1 = []
    predicted_group_2 = []

    # Get today's date to replace last week's date for normalization
    today_date = last_timestamp.date()

    # Normalize and combine crowd sizes for predictions based on last week's data
    for i in last_week_indices:
        # Apply combination logic from main2 for both groups
        if special_ap in aps_history_7d and i < len(aps_history_7d[special_ap]) and aps_history_7d[special_ap][i] > 50:
            crowd_size_group_1 = sum((aps_history_7d[ap][i] for ap in additional_aps if ap in aps_history_7d), aps_history_7d[special_ap][i])
        else:
            crowd_size_group_1 = aps_history_7d[special_ap][i] if special_ap in aps_history_7d else 0

        crowd_size_group_2 = sum(aps_history_7d[ap][i] for ap in group_2 if ap in aps_history_7d)

        # Normalize these values using linear scaling
        last_group_1_value = combined_group_1[-1]['y'] if combined_group_1 else 1  # Avoid division by zero
        last_group_2_value = combined_group_2[-1]['y'] if combined_group_2 else 1

        if predicted_group_1:
            previous_group_1_value = predicted_group_1[-1]['y']
        else:
            previous_group_1_value = crowd_size_group_1

        if predicted_group_2:
            previous_group_2_value = predicted_group_2[-1]['y']
        else:
            previous_group_2_value = crowd_size_group_2

        # Apply linear scaling for normalization
        if previous_group_1_value > 0:  # Avoid division by zero
            normalized_group_1_value = last_group_1_value * (crowd_size_group_1 / previous_group_1_value)
        else:
            normalized_group_1_value = crowd_size_group_1

        if previous_group_2_value > 0:  # Avoid division by zero
            normalized_group_2_value = last_group_2_value * (crowd_size_group_2 / previous_group_2_value)
        else:
            normalized_group_2_value = crowd_size_group_2

        # Correct the date while keeping the time
        previous_datetime = aps_datetimes_7d[i]
        correct_datetime = datetime.combine(today_date, previous_datetime.time())  # Replace last week's date with today's date, keep the time

        # Store the predicted values
        predicted_group_1.append({"x": correct_datetime.isoformat(), "y": int(normalized_group_1_value)})
        predicted_group_2.append({"x": correct_datetime.isoformat(), "y": int(normalized_group_2_value)})

    # Extract the 'y' values from the predictions to apply smoothing
    group_1_y_values = [point['y'] for point in predicted_group_1]
    group_2_y_values = [point['y'] for point in predicted_group_2]

    # Apply moving average smoothing
    smoothed_group_1_y = moving_average(group_1_y_values, smoothing_window)
    smoothed_group_2_y = moving_average(group_2_y_values, smoothing_window)

    # Trim the datetime values to match the smoothed arrays
    smoothed_group_1 = [{"x": predicted_group_1[i + smoothing_window // 2]['x'], "y": int(smoothed_group_1_y[i])}
                        for i in range(len(smoothed_group_1_y))]
    smoothed_group_2 = [{"x": predicted_group_2[i + smoothing_window // 2]['x'], "y": int(smoothed_group_2_y[i])}
                        for i in range(len(smoothed_group_2_y))]

    return smoothed_group_1, smoothed_group_2


def get_previous_day_predictions(aps_history, aps_datetimes, special_ap, additional_aps, group_2, combined_group_1, combined_group_2, smoothing_window=5):
    # Fetch data for the last 48 hours
    aps_history_48h, aps_datetimes_48h = get_data(hours=48)

    # Define the time range for prediction: same 2-hour period from yesterday
    last_timestamp = aps_datetimes[-1]
    start_prediction_time = last_timestamp - timedelta(days=1)
    end_prediction_time = start_prediction_time + timedelta(hours=2)

    # Find the indices for the previous day's relevant time frame
    previous_day_indices = [i for i, dt in enumerate(aps_datetimes_48h) if start_prediction_time <= dt <= end_prediction_time]

    # Initialize lists for previous day prediction data
    predicted_group_1 = []
    predicted_group_2 = []

    # Get today's date
    today_date = last_timestamp.date()

    # Normalize and combine crowd sizes for predictions based on previous day's data
    for i in previous_day_indices:
        # Apply combination logic from main2 for both groups
        if special_ap in aps_history_48h and i < len(aps_history_48h[special_ap]) and aps_history_48h[special_ap][i] > 50:
            crowd_size_group_1 = sum((aps_history_48h[ap][i] for ap in additional_aps if ap in aps_history_48h), aps_history_48h[special_ap][i])
        else:
            crowd_size_group_1 = aps_history_48h[special_ap][i] if special_ap in aps_history_48h else 0

        crowd_size_group_2 = sum(aps_history_48h[ap][i] for ap in group_2 if ap in aps_history_48h)

        # Normalize these values to ensure smooth continuation from today's last point
        last_group_1_value = combined_group_1[-1]['y'] if combined_group_1 else 0
        last_group_2_value = combined_group_2[-1]['y'] if combined_group_2 else 0

        if predicted_group_1:
            previous_group_1_value = predicted_group_1[-1]['y']
        else:
            previous_group_1_value = crowd_size_group_1

        if predicted_group_2:
            previous_group_2_value = predicted_group_2[-1]['y']
        else:
            previous_group_2_value = crowd_size_group_2

        # Normalize the crowd size
        normalized_group_1_value = last_group_1_value + (crowd_size_group_1 - previous_group_1_value)
        normalized_group_2_value = last_group_2_value + (crowd_size_group_2 - previous_group_2_value)

        # Correct the date while keeping the time
        previous_datetime = aps_datetimes_48h[i]
        correct_datetime = datetime.combine(today_date, previous_datetime.time())  # Replace date with today's date, keep the time

        # Store the predicted values
        predicted_group_1.append({"x": correct_datetime.isoformat(), "y": int(normalized_group_1_value)})
        predicted_group_2.append({"x": correct_datetime.isoformat(), "y": int(normalized_group_2_value)})

    # Extract the 'y' values from the predictions to apply smoothing
    group_1_y_values = [point['y'] for point in predicted_group_1]
    group_2_y_values = [point['y'] for point in predicted_group_2]

    # Apply moving average smoothing
    smoothed_group_1_y = moving_average(group_1_y_values, smoothing_window)
    smoothed_group_2_y = moving_average(group_2_y_values, smoothing_window)

    # Trim the datetime values to match the smoothed arrays
    smoothed_group_1 = [{"x": predicted_group_1[i + smoothing_window // 2]['x'], "y": int(smoothed_group_1_y[i])}
                        for i in range(len(smoothed_group_1_y))]
    smoothed_group_2 = [{"x": predicted_group_2[i + smoothing_window // 2]['x'], "y": int(smoothed_group_2_y[i])}
                        for i in range(len(smoothed_group_2_y))]

    return smoothed_group_1, smoothed_group_2

def main2():
    # Load environment variables from .env file
    load_dotenv()

    # Fetch data for the last 6 hours
    aps_history, aps_datetimes = get_data(hours=6)

    # Define the groups of APs to combine
    special_ap = "R0_EST-AP_0.3"
    additional_aps = ["R0_EST-AP_0.4", "R0_AMF-AP_0.3"]
    group_2 = ["R0_EST-AP_0.2", "R0_EST-AP_0.1"]

    # Initialize lists to hold the combined results for each group
    combined_group_1 = []
    combined_group_2 = []

    # Combine crowd sizes for each group based on current data
    for i, datetime_value in enumerate(aps_datetimes):
        if special_ap in aps_history and i < len(aps_history[special_ap]) and aps_history[special_ap][i] > 50:
            crowd_size_group_1 = sum((aps_history[ap][i] for ap in additional_aps if ap in aps_history), aps_history[special_ap][i])
        else:
            crowd_size_group_1 = aps_history[special_ap][i] if special_ap in aps_history else 0

        crowd_size_group_2 = sum(aps_history[ap][i] for ap in group_2 if ap in aps_history)

        combined_group_1.append({"x": datetime_value.isoformat(), "y": crowd_size_group_1})
        combined_group_2.append({"x": datetime_value.isoformat(), "y": crowd_size_group_2})

    # Get future predictions using the previous day's data
    future_combined_group_1, future_combined_group_2 = get_last_week_predictions(aps_history, aps_datetimes, special_ap, additional_aps, group_2, combined_group_1, combined_group_2)

    # Plot historical and predicted data for both groups
    #plot_historical_and_predicted(future_combined_group_1, combined_group_1, "Group 1")
    #plot_historical_and_predicted(future_combined_group_2, combined_group_2, "Group 2")

    # Write the historical and future data separately
    write_to_js_file(combined_group_1, combined_group_2, future_combined_group_1[1:], future_combined_group_2[1:])


def plot_historical_and_predicted( future_data_unsorted,historical_data_unsorted, group_name):
    # Prepare the data for plotting
    historical_data=sorted(historical_data_unsorted,key= lambda x:x["x"])
    historical_dates = [entry["x"] for entry in historical_data]
    historical_values = [entry["y"] for entry in historical_data]
    future_data=sorted(future_data_unsorted,key= lambda x:x["x"])
    future_dates = [entry["x"] for entry in future_data[0:]]
    future_values = [entry["y"] for entry in future_data[0:]]

    plt.figure(figsize=(12, 6))
    
    # Plot historical data
    plt.plot(historical_dates, historical_values, label='Historical Data', marker='o')
    
    # Plot future predictions
    plt.plot(future_dates, future_values, label='Predicted Data', linestyle='--', marker='x', color='orange')

    plt.title(f'Crowd Size Prediction for {group_name}')
    plt.xlabel('Datetime')
    plt.ylabel('Crowd Size')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.show()



def write_to_js_file(historic_group_1, historic_group_2, future_group_1, future_group_2):
    # Sort historical data by datetime
    historic_group_1.sort(key=lambda x: x["x"])
    historic_group_2.sort(key=lambda x: x["x"])

    # Sort future data by datetime
    future_group_1.sort(key=lambda x: x["x"])
    future_group_2.sort(key=lambda x: x["x"])

    # Prepare the JavaScript content for historical and future data
    js_content = (
        f"var historic_group1 = {json.dumps(historic_group_1, separators=(',', ':'))};\n"
        f"var historic_group2 = {json.dumps(historic_group_2, separators=(',', ':'))};\n"
        f"var future_group1 = {json.dumps(future_group_1, separators=(',', ':'))};\n"
        f"var future_group2 = {json.dumps(future_group_2, separators=(',', ':'))};\n"
    )

    # Write the content to a .js file
    with open("output_data.js", "w") as js_file:
        js_file.write(js_content)

    print("Data successfully written to output_data.js")



# Call main2 to execute and write the JS file
if __name__ == "__main__":
    main2()