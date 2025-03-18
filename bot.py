import os
import time
import random
import subprocess
from datetime import datetime
from content_generator import generate_content
from config import REPO_PATH, FILE_NAME, COMMIT_MESSAGES

def git_command(cmd):
    """Run a git command in the repo directory."""
    return subprocess.run(cmd, cwd=REPO_PATH, shell=True, capture_output=True, text=True)

def make_commit():
    """Generate content, commit, and push."""
    file_path = os.path.join(REPO_PATH, FILE_NAME)
    
    # Generate unique content
    with open(file_path, 'a') as f:
        f.write(generate_content() + '\n')
    
    # Git operations
    git_command("git pull --rebase")  # Avoid merge conflicts
    git_command(f"git add {FILE_NAME}")
    commit_msg = random.choice(COMMIT_MESSAGES)
    git_command(f'git commit -m "{commit_msg}"')
    git_command("git push")
    
    print(f"Committed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Execute ten commits at random times in a day."""
    for _ in range(10):
        make_commit()
        sleep_time = random.randint(1800, 7200)  # 30 min to 2 hours
        print(f"Next commit in {sleep_time // 60} minutes")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
