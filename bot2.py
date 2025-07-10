import os
import random
import subprocess
import time
from datetime import datetime

# Configuration
BASE_PATH = "/Users/app/Documents"  # Base directory for repositories
LOG_FILE = os.path.join(BASE_PATH, "multi_repo_bot_log.txt")  # Log file outside the repos

# List of repositories to manage
REPOSITORIES = [
    {
        "url": "https://github.com/meharsarmad786/autogit.git",
        "name": "autogit",
        "dummy_file": "dummy_file_{}.txt"  # Template for dummy files
    },
    {
        "url": "https://github.com/meharsarmad786/loomviztory.git",
        "name": "loomviztory",
        "dummy_file": "dummy_file_{}.txt"
    },
    {
        "url": "https://github.com/meharsarmad786/test.git",
        "name": "test",
        "dummy_file": "dummy_file_{}.txt"
    },
    {
        "url": "https://github.com/meharsarmad786/foodies",
        "name": "foodies",
        "dummy_file": "dummy_file_{}.txt"
    },
    {
        "url": "https://github.com/meharsarmad786/DinnerDash.git",
        "name": "DinnerDash",
        "dummy_file": "dummy_file_{}.txt"
    },
    {
        "url": "https://github.com/meharsarmad786/firebase-demo.git",
        "name": "firebase-demo",
        "dummy_file": "dummy_file_{}.txt"
    }
]

COMMIT_MESSAGES = [
    "Add dummy content",
    "Update repository files",
    "Automated commit",
    "Generate test content",
    "Daily update",
    "Periodic code update",
    "Maintain repository activity"
]

def log_message(message):
    """Append a message to the log file with a timestamp."""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

def git_command(cmd, repo_path):
    """Run a git command in the specified repo directory and handle errors."""
    try:
        result = subprocess.run(
            cmd, cwd=repo_path, shell=True, capture_output=True, text=True, check=True
        )
        log_message(f"[{os.path.basename(repo_path)}] Command '{cmd}' output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_message(f"[{os.path.basename(repo_path)}] Error running command: {cmd}\nSTDERR: {e.stderr}")
        raise

def clone_repo_if_needed(repo):
    """Clone repository if it doesn't exist locally."""
    repo_path = os.path.join(BASE_PATH, repo["name"])
    
    if not os.path.exists(repo_path):
        log_message(f"Cloning repository {repo['url']} to {repo_path}...")
        os.makedirs(BASE_PATH, exist_ok=True)
        
        try:
            subprocess.run(
                f"git clone {repo['url']} {repo_path}",
                shell=True, check=True, capture_output=True, text=True
            )
            log_message(f"Repository {repo['name']} cloned successfully.")
        except subprocess.CalledProcessError as e:
            log_message(f"Failed to clone repository {repo['name']}: {e.stderr}")
            return None
    else:
        log_message(f"Repository {repo['name']} already exists locally.")
    
    return repo_path

def create_dummy_content(repo):
    """Create or update a dummy file with unique content."""
    repo_path = os.path.join(BASE_PATH, repo["name"])
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = repo["dummy_file"].format(timestamp)
    file_path = os.path.join(repo_path, file_name)
    
    # Generate unique content
    content = f"This is an automated test file generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
    content += f"Random data: {random.randint(10000, 99999)}\n"
    
    # Write content to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    # Also update a timestamp.txt file to ensure at least one file is always modified
    with open(os.path.join(repo_path, "timestamp.txt"), 'w') as f:
        f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    log_message(f"[{repo['name']}] Created dummy file: {file_name}")
    return file_path

def make_commit_for_repo(repo):
    """Generate dummy content, commit, and push to GitHub for a specific repository."""
    repo_path = clone_repo_if_needed(repo)
    if not repo_path:
        log_message(f"Skipping repository {repo['name']} due to cloning failure.")
        return
    
    try:
        # Pull latest changes first
        log_message(f"[{repo['name']}] Pulling latest changes...")
        git_command("git pull", repo_path)
        
        # Create dummy content
        create_dummy_content(repo)
        
        # Check git status
        log_message(f"[{repo['name']}] Checking git status...")
        git_command("git status", repo_path)
        
        # Stage all modified files
        log_message(f"[{repo['name']}] Adding all modified files to commit...")
        git_command("git add .", repo_path)
        
        # Check if there are changes to commit
        status = git_command("git status", repo_path)
        if "nothing to commit" in status:
            log_message(f"[{repo['name']}] No changes to commit. Skipping.")
            return
        
        # Commit changes
        commit_msg = random.choice(COMMIT_MESSAGES)
        log_message(f"[{repo['name']}] Committing with message: {commit_msg}")
        git_command(f'git commit -m "{commit_msg}"', repo_path)
        
        # Push changes
        log_message(f"[{repo['name']}] Pushing changes to GitHub...")
        git_command("git push", repo_path)
        
        log_message(f"[{repo['name']}] ✅ Committed and pushed successfully.")
    
    except subprocess.CalledProcessError as e:
        log_message(f"[{repo['name']}] Failed during git operations: {e}")
        # Try to recover
        try:
            log_message(f"[{repo['name']}] Attempting to recover with stash-pull-pop strategy...")
            git_command("git stash", repo_path)
            git_command("git pull --rebase", repo_path)
            git_command("git stash pop", repo_path)
            # Retry commit and push
            git_command("git add .", repo_path)
            commit_msg = random.choice(COMMIT_MESSAGES) + " (retry)"
            git_command(f'git commit -m "{commit_msg}"', repo_path)
            git_command("git push", repo_path)
            log_message(f"[{repo['name']}] ✅ Recovered and pushed successfully.")
        except Exception as recovery_error:
            log_message(f"[{repo['name']}] Recovery failed: {recovery_error}")
    except Exception as e:
        log_message(f"[{repo['name']}] Unexpected error: {e}")

def process_all_repositories(interval_minutes=21600):
    """Process all repositories with a delay between each."""
    log_message(f"Starting multi-repository commit bot (interval: {interval_minutes} minutes)...")
    
    while True:
        try:
            for repo in REPOSITORIES:
                log_message(f"Processing repository: {repo['name']}")
                make_commit_for_repo(repo)
                
                # Short delay between repositories to avoid overwhelming
                log_message("Waiting 30 seconds before processing next repository...")
                time.sleep(21600)
            
            # Wait for the specified interval before the next round
            next_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_message(f"⏳ All repositories processed. Next run at {next_run} (in {interval_minutes} minutes)...")
            time.sleep(interval_minutes * 43200)
            
        except KeyboardInterrupt:
            log_message("Script stopped by user.")
            break
        except Exception as e:
            log_message(f"Unexpected error in main loop: {e}. Continuing after short delay...")
            time.sleep(60)  # Brief pause before retrying to avoid rapid error loops

if __name__ == "__main__":
    process_all_repositories(interval_minutes=5)  # Default to 30 minutes between cycles 