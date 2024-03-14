
#for demo purposes
import csv

def read_csv_to_2d_list(filepath):
    """
    Reads a CSV file and converts it to a 2D list.
    
    Args:
        filepath (str): The path to the CSV file to be read.
        
    Returns:
        list: A 2D list where each sublist represents a row from the CSV file.
    """
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data
##

#init 
import requests
broker_address="150.140.186.118:1026"
owner="Estia_Rio_1"

def make_request_to_wlc():
    data=[]
    #demo payload
    data=read_csv_to_2d_list("get_data/demo_payload.csv")
    #

    return data


import requests  # Ensure requests is imported to use it for HTTP requests

def get_access_points_by_owner(owner, broker_address):
    # Define the base URL of the Context Broker and the endpoint
    base_url = "http://" + broker_address
    endpoint = "/entities"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Include a limit in the query parameters
    params = {
        "type": "AccessPoint",
        "q": f"owner=={owner}",  # Query filter for entities of type AccessPoint with a specified owner
        "limit": 999  # Limit the number of entities to be returned
    }

    response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)

    # Check if the request was successful
    if 200 <= response.status_code < 300:
        # Parse the JSON response into a Python structure
        data = response.json()
        # Extract and return the list of IDs
        return [entity['id'] for entity in data]
    else:
        # Handle potential errors (e.g., connection problems, authentication issues)
        return f"Failed to retrieve entities: {response.status_code}, {response.text}"






def update_access_point(entity_id, broker_address,measurement):
    base_url = "http://"+broker_address
    endpoint = f"/entities/{entity_id}/attrs"
    headers = {"Content-Type": "application/json"}
    updates = {
        "measurement": {
            "value": measurement,  
            "type": "StructuredValue"  # Indicating that the measurement contains structured data
        }
    }
    response = requests.patch(f"{base_url}{endpoint}", json=updates, headers=headers)
    if 200 <= response.status_code < 300:
        return "AccessPoint updated successfully."
    else:
        return f"Failed to update AccessPoint: {response.status_code} - {response.text}"

def create_access_point(entity_id, broker_address, measurement,owner):
    base_url = "http://"+broker_address
    endpoint = f"/entities"
    headers = {"Content-Type": "application/json"}
    data = {
            "id": entity_id,
            "type": "AccessPoint",
            "owner": {
                "value": owner,
                "type": "Text"
            },
            "measurement": {
                "value": measurement,
                "type": "StructuredValue"
            }
        }
    response = requests.post(f"{base_url}{endpoint}", json=data, headers=headers)
    if 200 <= response.status_code < 300:
        return "AccessPoint created successfully."
    else:
        return f"Failed to create AccessPoint: {response.status_code} - {response.text}"