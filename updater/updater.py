import base64
from github import Github
import schedule
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from environment variable
github_token = os.getenv('GITHUB_TOKEN')

# Initialize GitHub with the token
g = Github(github_token)

# Replace 'your_username', 'your_repo', and 'your_file_path'
repo = g.get_repo("Skorpinakos/estia-updater")
file_path = "update_file.html"

def update_file():
    try:
        # Attempt to retrieve the existing file
        contents = repo.get_contents(file_path)
        # This is the content you want to update to, change as needed
        new_contents = "Updated content " + time.ctime()
        # Update the file in the repository
        repo.update_file(contents.path, "Update file", new_contents, contents.sha)
        print(f"File updated at {time.ctime()}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the function to run every 2 minutes
schedule.every(2).minutes.do(update_file)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
