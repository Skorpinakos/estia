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

            return aps_history, aps_datetimes

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def main(plot=False):
    # Load environment variables from .env file
    load_dotenv()
    aps_history, aps_datetimes = get_data(hours=48)

    # Parse the locations
    locations_filepath = "locations.txt"
    locations = parse_locations(locations_filepath)

    # Filter aps_history to only include spots present in locations
    filtered_aps_history = {spot: aps_history[spot] for spot in aps_history if spot in locations}

    # Save filtered aps_history into a list and print the result
    filtered_aps_history_list = list(filtered_aps_history.items())

    # Print the filtered APs
    for spot, history in filtered_aps_history_list:
        print(f"Spot: {spot}, History: {history}")

    if plot==True:
        plot_spots_with_map(aps_history, aps_datetimes , locations_filepath, margin=2)
    return aps_datetimes,filtered_aps_history_list


def main2():
    # Load environment variables from .env file
    load_dotenv()

    # Fetch data for the last 2 hours
    aps_history, aps_datetimes = get_data(hours=2)

    # Define the groups of APs to combine
    group_1 = ["R0_EST-AP_0.3", "R0_EST-AP_0.4", "R0_AMF-AP_0.3"]
    group_2 = ["R0_EST-AP_0.2", "R0_EST-AP_0.1"]

    # Initialize lists to hold the combined results for each group
    combined_group_1 = []
    combined_group_2 = []

    # Iterate over the datetimes to build the combined crowd sizes for each group
    for i, datetime_value in enumerate(aps_datetimes):
        # Initialize crowd sizes for this datetime
        crowd_size_group_1 = 0
        crowd_size_group_2 = 0

        # Combine crowd sizes for group 1
        for ap in group_1:
            if ap in aps_history and i < len(aps_history[ap]):
                crowd_size_group_1 += aps_history[ap][i]

        # Combine crowd sizes for group 2
        for ap in group_2:
            if ap in aps_history and i < len(aps_history[ap]):
                crowd_size_group_2 += aps_history[ap][i]

        # Append results as JSON objects with 'x' and 'y' keys
        combined_group_1.append({"x": datetime_value.isoformat(), "y": crowd_size_group_1})
        combined_group_2.append({"x": datetime_value.isoformat(), "y": crowd_size_group_2})

    # Write the results to a JavaScript file
    write_to_js_file(combined_group_1, combined_group_2)


def write_to_js_file(group_1_data, group_2_data):
    # Prepare the JavaScript content as strings (one line per element)
    js_content = f"""
    var group1 = {json.dumps(group_1_data, separators=(',', ':'))};
    var group2 = {json.dumps(group_2_data, separators=(',', ':'))};
    """

    # Write the content to a .js file
    with open("output_data.js", "w") as js_file:
        js_file.write(js_content)

    print("Data successfully written to output_data.js")



# Call main2 to execute and write the JS file
if __name__ == "__main__":
    main2()