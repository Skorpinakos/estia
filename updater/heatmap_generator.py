import mysql.connector
import pandas as pd
import json
import re
import folium
from folium.plugins import HeatMap
import numpy as np

# Database connection details
db_config = {
    'host': '150.140.186.118',
    'port': 3306,
    'user': 'readonly_student',
    'password': 'iot_password',
    'database': 'default'
}


def generate_heatmap_html(table_name, start_date, exclude_topic="testing", noise_meters=0, seed=42):
    """
    Fetches data from the specified table, processes GPS data with added noise, and generates a heatmap.
    Returns the HTML content of the heatmap as a string.
    """
    try:
        # Establish the connection to the database
        connection = mysql.connector.connect(**db_config)
        query = f"""
            SELECT timestamp, topic, message
            FROM {table_name}
            WHERE timestamp >= %s
            AND topic NOT LIKE %s
        """
        # Execute the query
        data = pd.read_sql(query, connection, params=[start_date, f'%{exclude_topic}%'])
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if connection.is_connected():
            connection.close()

    # Parse 'message' column to extract GPS data
    def parse_location(location_field):
        """Extract latitude and longitude from mixed format location fields."""
        if isinstance(location_field, str):
            if "not available" in location_field:
                return None, None
            # Match latitude and longitude in string format
            match = re.search(r"Lat:\s*([-+]?\d*\.\d+),\s*Lon:\s*([-+]?\d*\.\d+)", location_field)
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                return latitude, longitude
        elif isinstance(location_field, dict):
            # Handle potential dictionary format (e.g., {"lat": ..., "lon": ...})
            return location_field.get("lat"), location_field.get("lon")
        return None, None

    # Convert JSON in 'message' column and extract GPS data
    data['message'] = data['message'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    data[['latitude', 'longitude']] = data['message'].apply(lambda x: pd.Series(parse_location(x.get('location'))))

    # Filter for valid GPS coordinates and add noise
    data = data.dropna(subset=['latitude', 'longitude'])
    if data.empty:
        print("No valid GPS points found.")
        return None

    np.random.seed(seed)  # Set seed for reproducibility

    # Add noise in degrees
    lat_noise = (np.random.uniform(-noise_meters, noise_meters, size=len(data)) / 111000)
    lon_noise = (np.random.uniform(-noise_meters, noise_meters, size=len(data)) / 85000)  # Approximate conversion

    data['latitude'] += lat_noise
    data['longitude'] += lon_noise

    # Create a list of GPS points with noise
    gps_points = data[['latitude', 'longitude']].values.tolist()
    print(len(gps_points))

    # Create a map centered around the average latitude and longitude
    center_lat = sum([point[0] for point in gps_points]) / len(gps_points)
    center_lon = sum([point[1] for point in gps_points]) / len(gps_points)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add the HeatMap layer
    HeatMap(gps_points).add_to(m)

    output_file = "heatmap.html"
    
    # Save the generated map directly to an HTML file
    m.save(output_file)
    
    # Read the HTML content from the saved file for returning or uploading
    with open(output_file, "r") as f:
        html_content = f.read()
    
    return html_content

if __name__ == "__main__":
    generate_heatmap_html("estia_visitors", "2024-10-01")
