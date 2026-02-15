@echo off
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not found in PATH.
    echo Please install Python manually from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    pause
    exit /b
)

echo Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    echo Please try running: python -m pip install flask
    pause
    exit /b
)

echo Setup complete!
echo You can now run the app with: python run.py
pause
