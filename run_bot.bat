@echo off
cd /d "C:\Users\M Saad\Desktop\iifa tech\Github commit bot"

REM Activate virtual environment
call venv\Scripts\activate

REM Run the Python bot
python bot.py

REM Deactivate virtual environment
deactivate

REM Keep the window open for debugging
pause
