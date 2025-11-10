@echo off
setlocal

set MODEL_FOLDER=models
set MODEL_FILE=de_core_news_lg-3.8.0-py3-none-any.whl
set MODEL_URL=https://github.com/explosion/spacy-models/releases/download/de_core_news_lg-3.8.0/de_core_news_lg-3.8.0-py3-none-any.whl

echo ---------------------------------------------
echo   Flask Setup + Virtual Environment + Model
echo ---------------------------------------------
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

:: STEP 2 — Check virtualenv module
python -m virtualenv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo virtualenv not found. Installing...
    python -m pip install virtualenv
)
echo virtualenv ready.
echo.

:: STEP 3 — Create venv if missing
if not exist "venv" (
    echo Creating virtual environment...
    python -m virtualenv venv
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

:: STEP 4 — Activate venv
echo Activating venv...
call venv\Scripts\activate
echo venv activated.
echo.

:: STEP 5 — Install requirements
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
) else (
    echo WARNING: requirements.txt not found!
    echo.
)

:: STEP 6 — Ensure model folder exists
if not exist "%MODEL_FOLDER%" (
    echo Creating model folder "%MODEL_FOLDER%"...
    mkdir "%MODEL_FOLDER%"
)

:: STEP 7 — Check model file and download if missing
if not exist "%MODEL_FOLDER%\%MODEL_FILE%" (
    echo spaCy model file not found! Downloading...
    python download_model.py
) else (
    echo spaCy model file already present.
)

:: STEP 8 — Install spaCy model from local wheel if not already installed
python -c "import de_core_news_lg" 2>nul
if %errorlevel% neq 0 (
    echo Installing spaCy model from local file...
    pip install --upgrade --no-deps "%MODEL_FOLDER%\%MODEL_FILE%"
) else (
    echo spaCy model already installed in venv.
)

:: STEP 9 — Run Flask app
echo Starting Flask app...
python runFlask.py

pause