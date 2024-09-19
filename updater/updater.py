import base64
from github import Github
import schedule
import time
from dotenv import load_dotenv
import os
from menu_processor_online import get_current_menus
from datetime import datetime
from metrics_calculator import main2  # Importing main2 function from metrics_calculator

class Var:
    def __init__(self,name,declaration_type,assigned_object_inline_text):
        self.name=name
        self.declaration_type=declaration_type
        self.assigned_object_inline_text=assigned_object_inline_text
        self.length=len(self.name)

def init():
    # Load environment variables from .env file
    load_dotenv()

    # Get the GitHub token from environment variable
    github_token = os.getenv('GITHUB_TOKEN')

    # Initialize GitHub with the token
    g = Github(github_token)

    # Replace 'your_username', 'your_repo', and 'your_file_path'
    repo = g.get_repo("Skorpinakos/estia")
    file_path = "data.js"
    return repo, file_path

def edit_variables(file_content, new_vars):
    lines = file_content.split("\n")
    leftovers = []

    for var in new_vars:
        leftover_flag = 1
        for i, line in enumerate(lines.copy()):
            if len(line.split(" ")) < 2:
                continue
            if line.strip().split(" ")[1][0:var.length] == var.name:
                print(f"found {var.name} in line {i}")
                lines[i] = f"{var.declaration_type} {var.name} = {var.assigned_object_inline_text}"
                leftover_flag = 0
                break
        if leftover_flag == 1:
            leftovers.append(var)

    for var in leftovers:
        line_text = f"{var.declaration_type} {var.name} = {var.assigned_object_inline_text}"
        lines = [line_text,] + lines

    return "\n".join(lines)

def read_output_data():
    """
    Reads the 'output_data.js' file, extracts variable declarations and returns them as a list of Var objects.
    """
    output_file_path = "output_data.js"
    new_vars = []

    try:
        with open(output_file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split(" ", 2)  # Splitting the line into type, variable name, and value
            if len(parts) == 3:
                var_type = parts[0]
                var_name = parts[1]
                var_value = parts[2]
                new_var = Var(name=var_name, declaration_type=var_type, assigned_object_inline_text=var_value)
                new_vars.append(new_var)

    except FileNotFoundError:
        print(f"File '{output_file_path}' not found.")
    
    return new_vars

def update_file(repo, file_path):

    # Get current date and time
    current_date = datetime.now()
    # Format the date and time to exclude microseconds
    formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")

    # Run main2 from metrics_calculator.py to generate output data
    main2()  # Running main2 function before updating the repo
    
    # Read the generated 'output_data.js' to get variables for the update
    output_vars = read_output_data()

    vars = []
    menus = get_current_menus()
    menus_var = Var("menus_text", "var", str(menus) + ";")
    time_var = Var("last_update_datetime", "var", '"' + formatted_date + '";')
    vars.append(menus_var)
    vars.append(time_var)

    # Include the output variables from 'output_data.js'
    vars.extend(output_vars)

    # Attempt to retrieve the existing file from the repo
    contents = repo.get_contents(file_path)
    # Decode the content from byte string to UTF-8 string
    file_content = contents.decoded_content.decode('utf-8')
    
    # Edit the file content by updating the variables
    new_content = edit_variables(file_content, vars)

    # Update the file in the repository
    repo.update_file(contents.path, f"Updated Webpage at {formatted_date}", new_content, contents.sha)
    print(f"File updated at {time.ctime()}")

def main(freq):

    repo, file_path = init()
    # Schedule the function to run initially and then every 'freq' seconds
    update_file(repo=repo, file_path=file_path)

    schedule.every(freq).seconds.do(update_file, repo, file_path)
    
    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(0.01)

# Run the script in an infinite loop with error handling
while True:
    try:
        main(freq=21600)  # 21600 seconds = 6 hours
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(360)  # Retry after 6 minutes
