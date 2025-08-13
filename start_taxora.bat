@echo off
echo ========================================
echo    Taxora - AI Finance Assistant
echo    Starting Application...
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Setting up backend...
cd backend

echo Installing backend dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo Checking environment configuration...
if not exist .env (
    echo WARNING: .env file not found. Copying from .env.example
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env with your IBM Watson API keys
    echo Press any key to continue after configuring your API keys...
    pause
)

echo.
echo Starting backend server...
start "Taxora Backend" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

cd ..\frontend

echo.
echo Installing frontend dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo Starting frontend application...
start "Taxora Frontend" cmd /k "streamlit run app.py --server.port 8501"

echo.
echo ========================================
echo    Taxora is starting up!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:8501
echo API Docs: http://localhost:8000/docs
echo.
echo Both services are starting in separate windows.
echo Close this window when you're done using Taxora.
echo.
pause
