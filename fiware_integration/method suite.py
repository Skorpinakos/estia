
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
        reader = csv.reader(file,delimiter=";")
        data = [row for row in reader]
    return data
##

#init 
import requests
import random
from collections import defaultdict
broker_address="150.140.186.118:1026"
facility="Estia_Rio_1"

def make_request_to_wlc():
    data=[]
    #demo payload
    data=read_csv_to_2d_list("fiware_integration/demo_payload.csv")
    #
    res=data
    new_measurement=defaultdict(list)
    header=res[0]
    for line in res[1:]:
        #print(len(line))
        temp_dict={}
        for i,item in enumerate(line):
            temp_dict[str(header[i])]=str(item)

        AP_name=temp_dict["hwWlanStaApName"]
        new_measurement[AP_name].append(temp_dict)
    return new_measurement




def get_sns_access_points_by_facility(facility, broker_address):
    # Define the base URL of the Context Broker and the endpoint
    base_url = "http://" + broker_address
    endpoint = "/v2/entities"



    # Include a limit in the query parameters
    params = {
        "type": "AccessPoint",
        "limit": 999  # Limit the number of entities to be returned, 999 is the max, default is 20.
    }

    response = requests.get(f"{base_url}{endpoint}",  params=params)
    

    # Check if the request was successful
    if 200 <= response.status_code < 300:
        # Parse the JSON response into a Python structure
        data = response.json()
        # Extract and return the list of IDs
        return [int(entity['id'].split(":")[-1]) for entity in data]
    elif 400<=response.status_code<=404:
        print("no entity found , returning sn of 0")
        return [0,]
    else:
        # Handle potential errors (e.g., connection problems, authentication issues)
        return f"Failed to retrieve entities: {response.status_code}, {response.text}"






def update_access_point(entity_id, broker_address,measurement):
    base_url = "http://"+broker_address
    endpoint = f"/v2/entities/{entity_id}/attrs"
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

def create_access_point(broker_address, measurement,facility, entity_id="default",name="default",loc="0,0"):
    if entity_id=="default":
        #ID FORMAT = AP:FACILITY:SN SN->serial number generated here
        entity_sn=max(max(get_sns_access_points_by_facility(facility=facility,broker_address=broker_address)),0)+1
        entity_id="AP:"+str(facility)+":"+str(entity_sn)
    else:
        if int(entity_id.split(":")[-1]) in get_sns_access_points_by_facility(facility=facility,broker_address=broker_address):
            print("already exists")
            update_access_point(entity_id=entity_id,broker_address=broker_address,measurement=measurement)
            return entity_id

    base_url = "http://"+broker_address
    endpoint = f"/v2/entities"
    headers = {"Content-Type": "application/json"}
    data = {
            "id": entity_id,
            "type": "AccessPoint",
            "facility": {
                "value": facility,
                "type": "Text"
            },
            "name": {
                "value": name,
                "type": "Text"
            },
            "measurement": {
                "value": measurement,
                "type": "StructuredValue"
            }
        }
    response = requests.post(f"{base_url}{endpoint}", json=data, headers=headers)
    if 200 <= response.status_code < 300:
        
        return entity_id
    else:
        return f"Failed to create AccessPoint: {response.status_code} - {response.text}"
    



    
new_measurement=make_request_to_wlc()
print(new_measurement.keys())
for AP in new_measurement.keys():
    print(len(new_measurement[AP]),AP)
    random.seed(AP)
    entity_id=create_access_point(broker_address=broker_address,measurement=new_measurement[AP],facility="test_estia",name=str(AP),entity_id="AP:"+"test_estia"+":"+str(random.randint(0,10**6)))
    print(entity_id)



exit()
print("my_print",entity_id)
print(update_access_point(entity_id=entity_id,broker_address=broker_address,measurement=make_request_to_wlc()))