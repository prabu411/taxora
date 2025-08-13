@echo off
echo ========================================
echo 🚀 Starting Taxora AI Finance Assistant
echo ========================================
echo.

echo 📦 Installing Streamlit dependencies...
pip install -r streamlit_requirements.txt

echo.
echo 🔧 Checking backend status...
curl -s http://127.0.0.1:8000/api/status >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Backend not running. Starting FastAPI backend...
    echo.
    start "Taxora Backend" cmd /k "cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
    echo ⏳ Waiting for backend to start...
    timeout /t 10 /nobreak >nul
) else (
    echo ✅ Backend is already running
)

echo.
echo 🌐 Starting Streamlit frontend...
echo 📱 Access your app at: http://localhost:8501
echo.
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

pause
