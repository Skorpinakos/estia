import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta




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

def get_previous_day_predictions(aps_history, aps_datetimes, special_ap, additional_aps, group_2, combined_group_1, combined_group_2, smoothing_window=10):
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
    future_combined_group_1, future_combined_group_2 = get_previous_day_predictions(aps_history, aps_datetimes, special_ap, additional_aps, group_2, combined_group_1, combined_group_2)

    # Plot historical and predicted data for both groups
    #plot_historical_and_predicted(future_combined_group_1, combined_group_1, "Group 1")
    #plot_historical_and_predicted(future_combined_group_2, combined_group_2, "Group 2")

    # Write the historical and future data separately
    write_to_js_file(combined_group_1, combined_group_2, future_combined_group_1[1:], future_combined_group_2[1:])


import matplotlib.dates as mdates
from datetime import datetime

def plot_historical_and_predicted(future_data_unsorted, historical_data_unsorted, group_name):
    # Prepare the data for plotting, converting string dates to datetime objects
    historical_data = sorted(historical_data_unsorted, key=lambda x: x["x"])
    historical_dates = [datetime.fromisoformat(entry["x"]) for entry in historical_data]  # Convert to datetime
    historical_values = [entry["y"] for entry in historical_data]

    future_data = sorted(future_data_unsorted, key=lambda x: x["x"])
    future_dates = [datetime.fromisoformat(entry["x"]) for entry in future_data]  # Convert to datetime
    future_values = [entry["y"] for entry in future_data]

    plt.figure(figsize=(12, 6))

    # Plot historical data
    plt.plot(historical_dates, historical_values, label='Historical Data', marker='o')

    # Plot future predictions
    plt.plot(future_dates, future_values, label='Predicted Data', linestyle='--', marker='x', color='orange')

    plt.title(f'Crowd Size Prediction for {group_name}')
    plt.xlabel('Datetime')
    plt.ylabel('Crowd Size')

    # Use a date formatter to make the x-axis readable
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    # Rotate the x-axis labels for better readability
    plt.gcf().autofmt_xdate()

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