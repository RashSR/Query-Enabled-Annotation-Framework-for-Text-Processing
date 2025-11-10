@echo off
setlocal

:: Check venv exists
if not exist "venv\Scripts\activate" (
    echo ERROR: No virtual environment found!
    echo Expected: venv\Scripts\activate
    echo.
    echo Create one using:
    echo     python -m venv venv
    pause
    exit /b
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Start Flask app
echo Starting Flask server...
python runFlask.py

pause
