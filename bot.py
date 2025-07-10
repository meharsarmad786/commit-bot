import os
import random
import subprocess
import time
from datetime import datetime

# Configuration
REPO_PATH = "/Users/app/Documents/git"  # Your repo path
FILE_NAME = "commit_log.txt"  # File to modify
LOG_FILE = "/Users/app/Documents/git_bot_log.txt"  # Log file outside the repo
COMMIT_MESSAGES = [
    "Add hourly update",
    "Update log file",
    "Hourly commit",
    "Minor changes",
    "Automated commit"
]

def log_message(message):
    """Append a message to the log file with a timestamp."""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

def git_command(cmd):
    """Run a git command in the repo directory and handle errors."""
    try:
        result = subprocess.run(
            cmd, cwd=REPO_PATH, shell=True, capture_output=True, text=True, check=True
        )
        log_message(f"Command '{cmd}' output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_message(f"Error running command: {cmd}\nSTDERR: {e.stderr}")
        raise

def make_commit():
    """Generate unique content, commit, and push to GitHub."""
    file_path = os.path.join(REPO_PATH, FILE_NAME)
    
    # Generate unique content with timestamp and random value
    content = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Random Value: {random.randint(1000, 9999)}\n"
    
    # Append content to file
    with open(file_path, 'a') as f:
        f.write(content)
    log_message(f"Wrote content to {file_path}: {content.strip()}")

    try:
        # Check git status
        log_message("Checking git status...")
        git_command("git status")

        # Stage all modified files
        log_message("Adding all modified files to commit...")
        git_command("git add .")

        # Commit changes (even if log file was modified)
        log_message("Adding all modified files again to ensure all changes are staged...")
        git_command("git add .")  # Double-add to catch any last-second changes

        # Check if there are changes to commit
        status = git_command("git status")
        if "nothing to commit" in status:
            log_message("No changes to commit. Skipping.")
            return

        # Commit changes
        commit_msg = random.choice(COMMIT_MESSAGES)
        log_message(f"Committing with message: {commit_msg}")
        git_command(f'git commit -m "{commit_msg}"')

        # Pull with rebase to sync with remote
        log_message("Pulling with rebase to sync with remote...")
        git_command("git pull --rebase")

        # Push changes
        log_message("Pushing changes to GitHub...")
        git_command("git push")

        log_message(f"✅ Committed and pushed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except subprocess.CalledProcessError as e:
        log_message(f"Commit failed: {e}")
        # Stash changes, pull, and retry
        log_message("Stashing changes to recover...")
        git_command("git stash")
        git_command("git pull --rebase")
        git_command("git stash pop")
        # Retry commit and push
        log_message("Retrying commit and push after stash...")
        git_command("git add .")
        git_command(f'git commit -m "{commit_msg} (retry)"')
        git_command("git push")
        log_message(f"✅ Recovered and pushed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Run commits every 2 minutes indefinitely."""
    log_message("Starting 2-minute interval commit bot...")
    while True:
        try:
            make_commit()
            log_message("⏳ Sleeping for 2 minutes...")
            time.sleep(21600)  # Sleep for 2 minutes (120 seconds)
        except KeyboardInterrupt:
            log_message("Script stopped by user.")
            break
        except Exception as e:
            log_message(f"Unexpected error: {e}. Continuing...")
            time.sleep(21600)  # Brief pause before retrying to avoid rapid error loops

if __name__ == "__main__":
    main()
