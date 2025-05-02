===================================================
🚀 GITHUB AUTO COMMIT BOT - WINDOWS & MACOS
===================================================
Happy Coding! 💻🚀s

This bot automates GitHub commits **10 times a day** at random intervals 
to keep your repository active.

---------------------------------------------------
📂 PROJECT STRUCTURE
---------------------------------------------------
Github Commit Bot/
│-- bot.py                -> Main script to automate commits
│-- config.py             -> Configuration file (repo path, commit messages)
│-- content_generator.py  -> Generates commit content
│-- commit_log.txt        -> File where commit data is stored
│-- run_bot.bat           -> Windows batch file to run the bot
│-- README.txt            -> Documentation (this file)
│-- venv/                 -> Virtual environment (ignored in .gitignore)

---------------------------------------------------
🛠️ PREREQUISITES (WINDOWS & MAC)
---------------------------------------------------
- **Python 3.x** installed (`python --version` or `python3 --version`)
- **Git installed** (`git --version`)
- **GitHub repository created** (Public)

===================================================
🖥️ WINDOWS SETUP
===================================================
1️⃣ **Install Python** (if not installed)
   - Download from https://www.python.org/downloads/
   - Ensure Python is added to the system PATH.

2️⃣ **Clone the Repository**

3️⃣ **Create and Activate Virtual Environment**

4️⃣ **Install Dependencies**

5️⃣ **Update the Repository Path in `config.py`**

6️⃣ **Run the Bot Manually**

7️⃣ **Run the Bot via Batch File (`run_bot.bat`)**

8️⃣ **Automate Using Windows Task Scheduler**
- Open **Task Scheduler** (`Win + R` → `taskschd.msc`)
- Click **Create Basic Task** → Name it **"GitHub Auto Commit"**
- Choose **Daily** and set a start time (e.g., 00:00)
- Select **Start a Program** → Browse → Select `run_bot.bat`
- Enable **"Run with highest privileges"** and **"Run task as soon as possible after a missed start"**
- Click **Finish** and test by clicking **Run**

✅ **Now your bot will run automatically on Windows!** 🚀

===================================================
🍏 MACOS SETUP
===================================================
1️⃣ **Install Python** (if not installed)

2️⃣ **Clone the Repository**

3️⃣ **Create and Activate Virtual Environment**

4️⃣ **Install Dependencies**

5️⃣ **Update the Repository Path in `config.py`**

6️⃣ **Run the Bot Manually**

7️⃣ **Automate Using `cron`**
- Open Terminal and run:
  ```
  crontab -e
  ```
- Add this line to schedule the bot to run every hour:
  ```
  0 * * * * /usr/bin/python3 /Users/yourusername/path/to/github-commit-bot/bot.py
  ```
- Save and exit (`CTRL+X`, then `Y`, then `Enter`)

✅ **Now your bot will run automatically on macOS!** 🚀

---------------------------------------------------
📌 .GITIGNORE (MUST INCLUDE)
---------------------------------------------------
Ensure these files are **ignored** in `.gitignore`:

---------------------------------------------------
🛠️ TROUBLESHOOTING
---------------------------------------------------
✅ **Windows: Task Scheduler Not Running?**
- Ensure the `.bat` file runs manually first.
- Open **Task Scheduler Logs** via `eventvwr.msc` → **TaskScheduler > Operational**.
- Enable **"Run whether user is logged in or not"**.

✅ **Mac: Cron Job Not Running?**
- Check cron logs:
- Ensure cron is enabled:

---------------------------------------------------
🎉 YOUR BOT IS NOW AUTOMATED! 🚀
---------------------------------------------------
This setup ensures **10 commits per day at random intervals** without conflicts.
For any issues, open an issue in the GitHub repository.

Happy Coding! 💻🚀
