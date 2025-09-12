import os
import random
import subprocess
import time
from datetime import datetime

# Configuration
BASE_PATH = "/Users/app/Downloads"  # Base directory for repositories
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
        error_msg = e.stderr.strip()
        log_message(f"[{os.path.basename(repo_path)}] Error running command: {cmd}\nSTDERR: {error_msg}")
        
        # Handle specific git errors
        if "Authentication failed" in error_msg or "fatal: Authentication failed" in error_msg:
            log_message(f"[{os.path.basename(repo_path)}] Authentication failed. Please check your git credentials.")
        elif "fatal: refusing to merge unrelated histories" in error_msg:
            log_message(f"[{os.path.basename(repo_path)}] Unrelated histories detected. This might need manual intervention.")
        elif "fatal: The current branch has no upstream branch" in error_msg:
            log_message(f"[{os.path.basename(repo_path)}] No upstream branch set. Setting upstream...")
            try:
                subprocess.run(f"git branch --set-upstream-to=origin/main main", cwd=repo_path, shell=True, check=True)
                log_message(f"[{os.path.basename(repo_path)}] Upstream branch set successfully.")
            except:
                log_message(f"[{os.path.basename(repo_path)}] Failed to set upstream branch.")
        
        raise

def initialize_new_repository(repo_path):
    """Initialize a new repository if it doesn't exist on GitHub yet."""
    try:
        log_message(f"[{os.path.basename(repo_path)}] Initializing new repository...")
        
        # Initialize git repository
        git_command("git init", repo_path)
        
        # Add remote origin
        remote_url = None
        for repo in REPOSITORIES:
            if repo["name"] == os.path.basename(repo_path):
                remote_url = repo["url"]
                break
        
        if remote_url:
            git_command(f"git remote add origin {remote_url}", repo_path)
        else:
            log_message(f"[{os.path.basename(repo_path)}] Could not find remote URL for repository.")
            return False
        
        # Create initial README
        readme_path = os.path.join(repo_path, "README.md")
        with open(readme_path, 'w') as f:
            f.write(f"# {os.path.basename(repo_path)}\n\nThis is an automated repository managed by the git bot.\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Add and commit README
        git_command("git add README.md", repo_path)
        git_command('git commit -m "Initial commit: Add README"', repo_path)
        
        # Create and switch to main branch
        git_command("git branch -M main", repo_path)
        
        # Push to GitHub
        git_command("git push -u origin main", repo_path)
        
        log_message(f"[{os.path.basename(repo_path)}] New repository initialized and pushed successfully.")
        return True
        
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Failed to initialize new repository: {e}")
        return False

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
            
            # Try to initialize as new repository
            log_message(f"Attempting to initialize {repo['name']} as new repository...")
            if initialize_new_repository(repo_path):
                log_message(f"Repository {repo['name']} initialized successfully.")
            else:
                log_message(f"Failed to initialize repository {repo['name']}.")
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

def cleanup_repo(repo_path):
    """Clean up the repository to ensure a clean working directory."""
    try:
        # Check if there are any untracked files
        status = git_command("git status --porcelain", repo_path)
        
        if status.strip():
            log_message(f"[{os.path.basename(repo_path)}] Cleaning up working directory...")
            
            # Stash any changes
            git_command("git stash", repo_path)
            
            # Remove any untracked files (be careful with this)
            git_command("git clean -fd", repo_path)
            
            # Pop stashed changes back
            git_command("git stash pop", repo_path)
            
            log_message(f"[{os.path.basename(repo_path)}] Cleanup completed.")
        else:
            log_message(f"[{os.path.basename(repo_path)}] Working directory is clean.")
            
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Cleanup failed: {e}")

def check_remote_status(repo_path):
    """Check if the remote repository is accessible and up to date."""
    try:
        # Check remote URL
        remote_url = git_command("git remote get-url origin", repo_path)
        log_message(f"[{os.path.basename(repo_path)}] Remote URL: {remote_url}")
        
        # Check if remote exists
        git_command("git remote -v", repo_path)
        
        # Fetch latest from remote
        log_message(f"[{os.path.basename(repo_path)}] Fetching latest from remote...")
        git_command("git fetch origin", repo_path)
        
        # Check branch status
        branch_status = git_command("git status -uno", repo_path)
        log_message(f"[{os.path.basename(repo_path)}] Branch status: {branch_status}")
        
        return True
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Remote status check failed: {e}")
        return False

def verify_push_success(repo_path):
    """Verify that the push was successful by checking remote status."""
    try:
        # Fetch latest from remote
        git_command("git fetch origin", repo_path)
        
        # Check if local and remote are in sync
        local_commit = git_command("git rev-parse HEAD", repo_path)
        remote_commit = git_command("git rev-parse origin/main", repo_path)
        
        if local_commit == remote_commit:
            log_message(f"[{os.path.basename(repo_path)}] ✅ Push verified: Local and remote are in sync.")
            return True
        else:
            log_message(f"[{os.path.basename(repo_path)}] ⚠️ Push verification failed: Local and remote commits differ.")
            return False
            
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Push verification failed: {e}")
        return False

def ensure_correct_branch(repo_path):
    """Ensure the repository is on the correct branch and handle any git state issues."""
    try:
        # Check current branch
        current_branch = git_command("git branch --show-current", repo_path)
        log_message(f"[{os.path.basename(repo_path)}] Current branch: {current_branch}")
        
        # If not on main branch, switch to it
        if current_branch != "main":
            log_message(f"[{os.path.basename(repo_path)}] Switching to main branch...")
            git_command("git checkout main", repo_path)
        
        # Check if we're in a detached HEAD state
        head_status = git_command("git status", repo_path)
        if "HEAD detached" in head_status:
            log_message(f"[{os.path.basename(repo_path)}] Detached HEAD detected. Switching to main...")
            git_command("git checkout main", repo_path)
        
        # Ensure we have a clean working directory
        git_command("git status", repo_path)
        
        return True
        
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Failed to ensure correct branch: {e}")
        return False

def reset_repo_to_clean_state(repo_path):
    """Reset the repository to a clean state if there are unresolvable conflicts."""
    try:
        log_message(f"[{os.path.basename(repo_path)}] Resetting repository to clean state...")
        
        # Stash any changes
        git_command("git stash", repo_path)
        
        # Reset to match remote
        git_command("git reset --hard origin/main", repo_path)
        
        # Clean untracked files
        git_command("git clean -fd", repo_path)
        
        # Pull latest changes
        git_command("git pull", repo_path)
        
        log_message(f"[{os.path.basename(repo_path)}] Repository reset completed.")
        return True
        
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Repository reset failed: {e}")
        return False

def check_and_resolve_conflicts(repo_path):
    """Check for merge conflicts and resolve them if possible."""
    try:
        # Check git status for conflicts
        status = git_command("git status", repo_path)
        
        if "You have unmerged paths" in status or "fix conflicts" in status:
            log_message(f"[{os.path.basename(repo_path)}] Merge conflicts detected. Attempting to resolve...")
            
            # Abort any ongoing merge
            git_command("git merge --abort", repo_path)
            
            # Reset to clean state
            git_command("git reset --hard HEAD", repo_path)
            
            # Pull with rebase to avoid merge commits
            git_command("git pull --rebase", repo_path)
            
            log_message(f"[{os.path.basename(repo_path)}] Conflicts resolved.")
            return True
        else:
            log_message(f"[{os.path.basename(repo_path)}] No conflicts detected.")
            return True
            
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Conflict resolution failed: {e}")
        return False

def test_git_authentication(repo_path):
    """Test if git authentication is working properly."""
    try:
        log_message(f"[{os.path.basename(repo_path)}] Testing git authentication...")
        
        # Test if we can fetch from remote
        git_command("git fetch origin", repo_path)
        
        # Test if we can push (dry run)
        try:
            git_command("git push --dry-run", repo_path)
            log_message(f"[{os.path.basename(repo_path)}] ✅ Authentication test passed.")
            return True
        except subprocess.CalledProcessError:
            log_message(f"[{os.path.basename(repo_path)}] ⚠️ Push test failed, but fetch works.")
            return True  # Fetch works, so basic auth is OK
            
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] ❌ Authentication test failed: {e}")
        return False

def ensure_repo_has_commits(repo_path):
    """Ensure the repository has at least one commit."""
    try:
        # Check if repository has any commits
        try:
            git_command("git log --oneline -1", repo_path)
            log_message(f"[{os.path.basename(repo_path)}] Repository has commits.")
            return True
        except subprocess.CalledProcessError:
            log_message(f"[{os.path.basename(repo_path)}] Repository appears to be empty. Creating initial commit...")
            
            # Create a README file
            readme_path = os.path.join(repo_path, "README.md")
            with open(readme_path, 'w') as f:
                f.write(f"# {os.path.basename(repo_path)}\n\nThis is an automated repository managed by the git bot.\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Add and commit the README
            git_command("git add README.md", repo_path)
            git_command('git commit -m "Initial commit: Add README"', repo_path)
            
            # Push the initial commit
            git_command("git push -u origin main", repo_path)
            
            log_message(f"[{os.path.basename(repo_path)}] Initial commit created and pushed.")
            return True
            
    except Exception as e:
        log_message(f"[{os.path.basename(repo_path)}] Failed to ensure repository has commits: {e}")
        return False

def re_clone_repository(repo):
    """Re-clone the repository if it's in an unrecoverable state."""
    try:
        repo_path = os.path.join(BASE_PATH, repo["name"])
        
        if os.path.exists(repo_path):
            log_message(f"[{repo['name']}] Re-cloning repository due to unrecoverable state...")
            
            # Remove the existing directory
            import shutil
            shutil.rmtree(repo_path)
            log_message(f"[{repo['name']}] Removed existing repository directory.")
        
        # Clone fresh
        log_message(f"[{repo['name']}] Cloning fresh copy of repository...")
        os.makedirs(BASE_PATH, exist_ok=True)
        
        subprocess.run(
            f"git clone {repo['url']} {repo_path}",
            shell=True, check=True, capture_output=True, text=True
        )
        
        log_message(f"[{repo['name']}] Repository re-cloned successfully.")
        return repo_path
        
    except Exception as e:
        log_message(f"[{repo['name']}] Failed to re-clone repository: {e}")
        return None

def make_commit_for_repo(repo):
    """Generate dummy content, commit, and push to GitHub for a specific repository."""
    repo_path = clone_repo_if_needed(repo)
    if not repo_path:
        log_message(f"Skipping repository {repo['name']} due to cloning failure.")
        return
    
    try:
        # Test git authentication first
        if not test_git_authentication(repo_path):
            log_message(f"[{repo['name']}] Git authentication failed. Skipping.")
            return
        
        # Check remote status first
        if not check_remote_status(repo_path):
            log_message(f"[{repo['name']}] Remote repository not accessible. Skipping.")
            return
        
        # Ensure we're on the correct branch
        if not ensure_correct_branch(repo_path):
            log_message(f"[{repo['name']}] Failed to ensure correct branch. Skipping.")
            return
        
        # Ensure repository has commits
        if not ensure_repo_has_commits(repo_path):
            log_message(f"[{repo['name']}] Failed to ensure repository has commits. Skipping.")
            return
        
        # Clean up the repository first
        cleanup_repo(repo_path)
        
        # Check and resolve any conflicts
        if not check_and_resolve_conflicts(repo_path):
            log_message(f"[{repo['name']}] Failed to resolve conflicts. Skipping.")
            return
        
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
        
        # Double-check staging
        log_message(f"[{repo['name']}] Verifying staged files...")
        git_command("git status", repo_path)
        
        # Check if there are changes to commit
        status = git_command("git status", repo_path)
        if "nothing to commit" in status:
            log_message(f"[{repo['name']}] No changes to commit. Skipping.")
            return
        
        # Commit changes
        commit_msg = random.choice(COMMIT_MESSAGES)
        log_message(f"[{repo['name']}] Committing with message: {commit_msg}")
        git_command(f'git commit -m "{commit_msg}"', repo_path)
        
        # Push changes to GitHub
        log_message(f"[{repo['name']}] Pushing changes to GitHub...")
        git_command("git push", repo_path)
        
        # Verify push was successful
        if verify_push_success(repo_path):
            log_message(f"[{repo['name']}] ✅ Committed and pushed successfully.")
        else:
            log_message(f"[{repo['name']}] ⚠️ Push completed but verification failed.")
    
    except subprocess.CalledProcessError as e:
        log_message(f"[{repo['name']}] Failed during git operations: {e}")
        # Try to recover with a more robust strategy
        try:
            log_message(f"[{repo['name']}] Attempting to recover with clean strategy...")
            
            # Stash any unstaged changes
            git_command("git stash", repo_path)
            
            # Pull latest changes
            git_command("git pull", repo_path)
            
            # Apply stashed changes
            git_command("git stash pop", repo_path)
            
            # Stage and commit again
            git_command("git add .", repo_path)
            commit_msg = random.choice(COMMIT_MESSAGES) + " (recovery)"
            git_command(f'git commit -m "{commit_msg}"', repo_path)
            
            # Push changes
            git_command("git push", repo_path)
            
            # Verify recovery push
            if verify_push_success(repo_path):
                log_message(f"[{repo['name']}] ✅ Recovered and pushed successfully.")
            else:
                log_message(f"[{repo['name']}] ⚠️ Recovery push completed but verification failed.")
            
        except Exception as recovery_error:
            log_message(f"[{repo['name']}] Recovery failed: {recovery_error}")
            
            # Try repository reset as last resort
            try:
                log_message(f"[{repo['name']}] Attempting repository reset as last resort...")
                if reset_repo_to_clean_state(repo_path):
                    # Try the commit process again after reset
                    create_dummy_content(repo)
                    git_command("git add .", repo_path)
                    commit_msg = random.choice(COMMIT_MESSAGES) + " (post-reset)"
                    git_command(f'git commit -m "{commit_msg}"', repo_path)
                    git_command("git push", repo_path)
                    
                    if verify_push_success(repo_path):
                        log_message(f"[{repo['name']}] ✅ Repository reset and push successful.")
                    else:
                        log_message(f"[{repo['name']}] ⚠️ Repository reset completed but push verification failed.")
                else:
                    log_message(f"[{repo['name']}] Repository reset failed.")
                    
            except Exception as reset_error:
                log_message(f"[{repo['name']}] Repository reset also failed: {reset_error}")
                
                # Try re-cloning as absolute last resort
                try:
                    log_message(f"[{repo['name']}] Attempting to re-clone repository as absolute last resort...")
                    new_repo_path = re_clone_repository(repo)
                    if new_repo_path:
                        # Try the commit process again with fresh clone
                        create_dummy_content(repo)
                        git_command("git add .", new_repo_path)
                        commit_msg = random.choice(COMMIT_MESSAGES) + " (post-reclone)"
                        git_command(f'git commit -m "{commit_msg}"', new_repo_path)
                        git_command("git push", new_repo_path)
                        
                        if verify_push_success(new_repo_path):
                            log_message(f"[{repo['name']}] ✅ Repository re-cloned and push successful.")
                        else:
                            log_message(f"[{repo['name']}] ⚠️ Repository re-cloned but push verification failed.")
                    else:
                        log_message(f"[{repo['name']}] Repository re-cloning failed.")
                        
                except Exception as reclone_error:
                    log_message(f"[{repo['name']}] Repository re-cloning also failed: {reclone_error}")
                
    except Exception as e:
        log_message(f"[{repo['name']}] Unexpected error: {e}")

def check_git_credentials():
    """Check if git credentials are properly configured."""
    try:
        # Check git config
        result = subprocess.run(
            "git config --global --list", 
            shell=True, capture_output=True, text=True
        )
        
        if result.returncode == 0:
            config_output = result.stdout
            if "user.name" in config_output and "user.email" in config_output:
                log_message("✅ Git credentials are configured.")
                return True
            else:
                log_message("⚠️ Git credentials are missing. Please configure user.name and user.email.")
                return False
        else:
            log_message("❌ Failed to check git configuration.")
            return False
            
    except Exception as e:
        log_message(f"❌ Error checking git credentials: {e}")
        return False

def setup_git_credentials():
    """Set up basic git credentials if they're missing."""
    try:
        log_message("Setting up git credentials...")
        
        # Set default user name and email if not configured
        subprocess.run("git config --global user.name 'Git Bot'", shell=True, check=True)
        subprocess.run("git config --global user.email 'bot@example.com'", shell=True, check=True)
        
        log_message("✅ Git credentials set up successfully.")
        return True
        
    except Exception as e:
        log_message(f"❌ Failed to set up git credentials: {e}")
        return False

def check_ssh_configuration():
    """Check if SSH keys are properly configured for GitHub access."""
    try:
        # Check if SSH agent is running
        result = subprocess.run(
            "ssh-add -l", 
            shell=True, capture_output=True, text=True
        )
        
        if result.returncode == 0:
            if "no identities" in result.stdout.lower():
                log_message("⚠️ SSH agent is running but no keys are loaded.")
                return False
            else:
                log_message("✅ SSH keys are loaded in SSH agent.")
                return True
        else:
            log_message("⚠️ SSH agent is not running or no keys loaded.")
            return False
            
    except Exception as e:
        log_message(f"❌ Error checking SSH configuration: {e}")
        return False

def test_github_ssh_access():
    """Test SSH access to GitHub."""
    try:
        log_message("Testing SSH access to GitHub...")
        
        result = subprocess.run(
            "ssh -T git@github.com", 
            shell=True, capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0 or "successfully authenticated" in result.stderr:
            log_message("✅ SSH access to GitHub is working.")
            return True
        else:
            log_message(f"⚠️ SSH access to GitHub failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        log_message("⚠️ SSH connection to GitHub timed out.")
        return False
    except Exception as e:
        log_message(f"❌ Error testing SSH access to GitHub: {e}")
        return False

def check_https_token_configuration():
    """Check if HTTPS token is properly configured for GitHub access."""
    try:
        # Check if git credential helper is configured
        result = subprocess.run(
            "git config --global credential.helper", 
            shell=True, capture_output=True, text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            log_message("✅ Git credential helper is configured.")
            return True
        else:
            log_message("⚠️ Git credential helper not configured. HTTPS authentication may fail.")
            return False
            
    except Exception as e:
        log_message(f"❌ Error checking HTTPS token configuration: {e}")
        return False

def test_github_https_access():
    """Test HTTPS access to GitHub."""
    try:
        log_message("Testing HTTPS access to GitHub...")
        
        # Try to fetch from a public GitHub repository to test HTTPS access
        result = subprocess.run(
            "git ls-remote https://github.com/octocat/Hello-World.git", 
            shell=True, capture_output=True, text=True, timeout=15
        )
        
        if result.returncode == 0:
            log_message("✅ HTTPS access to GitHub is working.")
            return True
        else:
            log_message(f"⚠️ HTTPS access to GitHub failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        log_message("⚠️ HTTPS connection to GitHub timed out.")
        return False
    except Exception as e:
        log_message(f"❌ Error testing HTTPS access to GitHub: {e}")
        return False

def suggest_authentication_methods():
    """Suggest authentication methods for GitHub access."""
    log_message("\n" + "="*60)
    log_message("🔐 GITHUB AUTHENTICATION SETUP GUIDE")
    log_message("="*60)
    log_message("If you're experiencing authentication issues, try one of these methods:")
    log_message("")
    log_message("1. SSH KEY AUTHENTICATION (Recommended):")
    log_message("   - Generate SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'")
    log_message("   - Add to SSH agent: ssh-add ~/.ssh/id_ed25519")
    log_message("   - Add public key to GitHub: cat ~/.ssh/id_ed25519.pub")
    log_message("")
    log_message("2. HTTPS TOKEN AUTHENTICATION:")
    log_message("   - Create Personal Access Token on GitHub")
    log_message("   - Configure credential helper: git config --global credential.helper store")
    log_message("   - Use token as password when prompted")
    log_message("")
    log_message("3. CHECK CURRENT CONFIGURATION:")
    log_message("   - SSH keys: ssh-add -l")
    log_message("   - Git config: git config --global --list")
    log_message("   - Test SSH: ssh -T git@github.com")
    log_message("   - Test HTTPS: git ls-remote https://github.com/octocat/Hello-World.git")
    log_message("="*60 + "\n")

def process_all_repositories(interval_hours=4):
    """Process all repositories with a delay between each."""
    interval_seconds = interval_hours * 3600  # Convert hours to seconds
    log_message(f"Starting multi-repository commit bot (interval: {interval_hours} hours)...")
    
    # Check and set up git credentials
    if not check_git_credentials():
        log_message("Setting up git credentials...")
        setup_git_credentials()
    
    # Check SSH configuration
    ssh_ok = check_ssh_configuration()
    if not ssh_ok:
        log_message("⚠️ SSH keys not properly configured. Some repositories may fail to authenticate.")
    
    # Test GitHub SSH access
    ssh_access_ok = test_github_ssh_access()
    if not ssh_access_ok:
        log_message("⚠️ SSH access to GitHub failed. Please check your SSH key configuration.")
    
    # Check HTTPS token configuration
    https_ok = check_https_token_configuration()
    if not https_ok:
        log_message("⚠️ HTTPS token not properly configured. Some repositories may fail to authenticate.")
    
    # Test GitHub HTTPS access
    https_access_ok = test_github_https_access()
    if not https_access_ok:
        log_message("⚠️ HTTPS access to GitHub failed. Please check your token configuration.")
    
    # If both authentication methods failed, show setup guide
    if not (ssh_ok and ssh_access_ok) and not (https_ok and https_access_ok):
        suggest_authentication_methods()
    
    while True:
        try:
            for repo in REPOSITORIES:
                log_message(f"Processing repository: {repo['name']}")
                make_commit_for_repo(repo)
                
                # Short delay between repositories to avoid overwhelming
                log_message("Waiting 30 seconds between repositories...")
                time.sleep(30)
            
            # Wait for the specified interval before the next round
            from datetime import datetime, timedelta
            next_run = (datetime.now() + timedelta(hours=interval_hours)).strftime('%Y-%m-%d %H:%M:%S')
            log_message(f"⏳ All repositories processed. Next run at {next_run} (in {interval_hours} hours)...")
            time.sleep(interval_seconds)
            
        except KeyboardInterrupt:
            log_message("Script stopped by user.")
            break
        except Exception as e:
            log_message(f"Unexpected error in main loop: {e}. Continuing after short delay...")
            time.sleep(60)  # Brief pause before retrying to avoid rapid error loops

if __name__ == "__main__":
    process_all_repositories(interval_hours=4)  # Default to 4 hours between cycles (6 times per day) 