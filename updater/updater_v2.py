import base64
from github import Github
import schedule
import time
from dotenv import load_dotenv
import os
from menu_processor_online import get_current_menus
from datetime import datetime
from metrics_calculator import main2
from heatmap_generator import generate_heatmap_html  # Import heatmap generation function

from datetime import datetime, timedelta

class Var:
    def __init__(self, name, declaration_type, assigned_object_inline_text):
        self.name = name
        self.declaration_type = declaration_type
        self.assigned_object_inline_text = assigned_object_inline_text
        self.length = len(self.name)

def init():
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    g = Github(github_token)
    repo = g.get_repo("Skorpinakos/estia")
    return repo, "data.js", "heatmap.html"

def edit_variables(file_content, new_vars):
    lines = file_content.split("\n")
    leftovers = []
    for var in new_vars:
        leftover_flag = 1
        for i, line in enumerate(lines.copy()):
            if len(line.split(" ")) < 2:
                continue
            if line.strip().split(" ")[1][0:var.length] == var.name:
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
    output_file_path = "output_data.js"
    new_vars = []
    try:
        with open(output_file_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split(" ", 2)
            if len(parts) == 3:
                var_type = parts[0]
                var_name = parts[1]
                var_value = parts[2]
                new_var = Var(name=var_name, declaration_type=var_type, assigned_object_inline_text=var_value)
                new_vars.append(new_var)
    except FileNotFoundError:
        print(f"File '{output_file_path}' not found.")
    return new_vars

def update_file(repo, file_path, heatmap_path):
    global start
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    main2()
    output_vars = read_output_data()
    vars = []
    menus = get_current_menus()
    menus_var = Var("menus_text", "var", str(menus) + ";")
    time_var = Var("last_update_datetime", "var", '"' + formatted_date + '";')
    vars.append(menus_var)
    vars.append(time_var)
    vars.extend(output_vars)

    contents = repo.get_contents(file_path)
    file_content = contents.decoded_content.decode('utf-8')
    new_content = edit_variables(file_content, vars)
    new_content = new_content.replace(" = = ", " = ")
    repo.update_file(contents.path, f"Updated Webpage at {formatted_date}", new_content, contents.sha)
    print(f"data.js file updated at {time.ctime()}")


    if time.time()-start<=60*60*24:
        return
    start=time.time()


    generate_heatmap_html("estia_visitors", "2024-10-01")

    # Read the HTML content from the file directly as a UTF-8 string
    with open(heatmap_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Upload the HTML file to GitHub as plain text (UTF-8)
    try:
        # Check if the HTML file already exists in the repo
        contents = repo.get_contents(heatmap_path)
        # Update the existing file
        repo.update_file(heatmap_path, f"Updated heatmap at {datetime.now()}", html_content, contents.sha, branch="main")
    except:
        # If the file does not exist, create a new one
        repo.create_file(heatmap_path, f"Created heatmap at {datetime.now()}", html_content, branch="main")
    
    print("Heatmap HTML file uploaded successfully.")

def main(freq):
    repo, data_file_path, heatmap_file_path = init()
    update_file(repo=repo, file_path=data_file_path, heatmap_path=heatmap_file_path)
    schedule.every(freq).seconds.do(update_file, repo, data_file_path, heatmap_file_path)
    while True:
        schedule.run_pending()
        time.sleep(0.01)



start=time.time()
while True:
    try:
        main(freq=600)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(360)
