import base64
from github import Github
import schedule
import time
from dotenv import load_dotenv
import os

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
    #print(github_token)

    # Initialize GitHub with the token
    g = Github(github_token)

    # Replace 'your_username', 'your_repo', and 'your_file_path'
    repo = g.get_repo("Skorpinakos/estia")
    file_path = "script.js"
    return repo,file_path

def edit_variables(file_content,new_vars):
    lines=file_content.split("\n")
    leftovers=[]
    
    
    for var in new_vars:
        leftover_flag=1
        for i,line in enumerate(lines.copy()):
            if len(line.split(" "))<2:
                continue
            if line.split(" ")[1]==var.name:
                print("found "+var+" in line "+str(i))
                lines[i]=var.declaration_type+" "+var.name+" = "+var.assigned_object_inline_text
                leftover_flag=0
                break
        if leftover_flag==1:
            leftovers.append(var)
    
    for var in leftovers:
        line_text=var.declaration_type+" "+var.name+" = "+var.assigned_object_inline_text
        lines=[line_text,]+lines

    return "\n".join(lines)





def update_file(repo,file_path,vars):
    try:
        # Attempt to retrieve the existing file
        contents = repo.get_contents(file_path)
        # Decode the content from byte string to UTF-8 string
        file_content = contents.decoded_content.decode('utf-8')
        new_content=edit_variables(file_content,vars)
        print(new_content) 
        #new_contents = "Updated content " + time.ctime()
        # Update the file in the repository
        #repo.update_file(contents.path, "Updated file", new_contents, contents.sha)
        print(f"File updated at {time.ctime()}")
    except Exception as e:
        print(f"An error occurred: {e}")



def main(freq):
    repo,file_path=init()
    # Schedule the function to run every 2 minutes
    vars=[]
    test_var=Var("test_var","let","{[],[]}")
    vars.append(test_var)
    schedule.every(freq).seconds.do(update_file,repo,file_path,vars)
    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)

main(freq=10)