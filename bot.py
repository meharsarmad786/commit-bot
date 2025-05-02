import os
import random
import subprocess
from datetime import datetime

# Configuration
REPO_PATH = "/Users/app/Downloads/git"  # Your repo path
FILE_NAME = "commit_log.txt"  # File to modify
COMMIT_MESSAGES = [
    "Add daily update",
    "Update log file",
    "Daily commit",
    "Minor changes",
    "Automated commit"
]

def git_command(cmd):
    """Run a git command in the repo directory and handle errors."""
    try:
        result = subprocess.run(
            cmd, cwd=REPO_PATH, shell=True, capture_output=True, text=True, check=True
        )
        print(f"Command '{cmd}' output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}\nSTDERR: {e.stderr}")
        raise

def make_commit():
    """Generate unique content, commit, and push to GitHub."""
    file_path = os.path.join(REPO_PATH, FILE_NAME)
    
    # Generate unique content with timestamp and random value
    content = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Random Value: {random.randint(1000, 9999)}\n"
    
    # Append content to file
    with open(file_path, 'a') as f:
        f.write(content)
    print(f"Wrote content to {file_path}: {content.strip()}")

    try:
        # Check git status
        print("Checking git status...")
        git_command("git status")

        # Stage all modified files
        print("Adding all modified files to commit...")
        git_command("git add .")

        # Check if there are changes to commit
        status = git_command("git status")
        if "nothing to commit" in status:
            print("No changes to commit. Exiting.")
            return

        # Commit changes
        commit_msg = random.choice(COMMIT_MESSAGES)
        print(f"Committing with message: {commit_msg}")
        git_command(f'git commit -m "{commit_msg}"')

        # Pull with rebase to sync with remote
        print("Pulling with rebase to sync with remote...")
        git_command("git pull --rebase")

        # Push changes
        print("Pushing changes to GitHub...")
        git_command("git push")

        print(f"✅ Committed and pushed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except subprocess.CalledProcessError as e:
        print(f"Commit failed: {e}")
        # Instead of resetting, try to stash and retry
        print("Stashing changes to recover...")
        git_command("git stash")
        git_command("git pull --rebase")
        git_command("git stash pop")
        # Retry push after resolving
        print("Retrying push after stash...")
        git_command("git add .")
        git_command(f'git commit -m "{commit_msg}"')
        git_command("git push")
        print(f"✅ Recovered and pushed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Perform a single commit."""
    print(f"Starting daily commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    make_commit()

if __name__ == "__main__":
    main()