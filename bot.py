import os
import time
import random
import subprocess
from datetime import datetime
from content_generator import generate_content
from config import REPO_PATH, FILE_NAME, COMMIT_MESSAGES

def git_command(cmd):
    """Run a git command in the repo directory and handle errors."""
    result = subprocess.run(cmd, cwd=REPO_PATH, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def make_commit():
    """Generate unique content, commit, and push with conflict avoidance."""
    file_path = os.path.join(REPO_PATH, FILE_NAME)
    
    # Generate content with a timestamp to ensure uniqueness
    content = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {generate_content()}\n"
    
    # Only write to the file if content is new
    with open(file_path, 'a') as f:
        f.write(content)

    # Check if there are changes to commit
    result = git_command("git diff --stat")
    
    # If no changes, skip commit
    if "nothing to commit" in result.lower():
        print("No changes detected, skipping commit.")
        return
    
    # Git operations
    print("Stashing changes if any...")
    git_command("git stash")
    
    print("Pulling with rebase...")
    git_command("git pull --rebase")  # Avoid merge conflicts
    
    print(f"Adding {FILE_NAME} to commit...")
    git_command(f"git add {FILE_NAME}")
    
    commit_msg = random.choice(COMMIT_MESSAGES)
    print(f"Committing with message: {commit_msg}")
    git_command(f'git commit -m "{commit_msg}"')
    
    print("Pushing changes...")
    git_command("git push")
    
    print(f"✅ Committed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Perform 5 commits at random intervals in a day."""
    for _ in range(5):
        make_commit()
        sleep_time = 86400 // 5  # Sleep for about 4 hours between commits (24 hours / 5 commits)
        print(f"⏳ Next commit in {sleep_time // 3600} hours...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
