@echo off
setlocal

echo -----------------------------------------
echo   Flask Auto Setup + Virtual Environment
echo -----------------------------------------
echo.

:: STEP 1 — Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python and add it to PATH.
    pause
    exit /b
)
echo Python detected.
echo.

:: STEP 2 — Check if virtualenv is installed
python -m virtualenv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo virtualenv not found. Installing...
    python -m pip install virtualenv
)
echo virtualenv ready.
echo.

:: STEP 3 — Check or create venv
if not exist "venv" (
    echo Creating virtual environment...
    python -m virtualenv venv
)
echo Virtual environment ready.
echo.

:: STEP 4 — Activate venv
echo Activating venv...
call venv\Scripts\activate
echo venv activated.
echo.

:: STEP 5 — Install requirements
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    echo.
) else (
    echo WARNING: requirements.txt not found!
    echo Skipping dependency installation.
    echo.
)

:: STEP 6 — Run Flask app
echo Starting Flask app...
python runFlask.py

pause
