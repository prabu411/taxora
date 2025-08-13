#!/bin/bash

echo "========================================"
echo "🚀 Starting Taxora AI Finance Assistant"
echo "========================================"
echo

echo "📦 Installing Streamlit dependencies..."
pip install -r streamlit_requirements.txt

echo
echo "🔧 Checking backend status..."
if ! curl -s http://127.0.0.1:8000/api/status > /dev/null 2>&1; then
    echo "⚠️  Backend not running. Starting FastAPI backend..."
    echo
    cd backend
    python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..
    echo "⏳ Waiting for backend to start..."
    sleep 10
else
    echo "✅ Backend is already running"
fi

echo
echo "🌐 Starting Streamlit frontend..."
echo "📱 Access your app at: http://localhost:8501"
echo

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# Cleanup on exit
if [ ! -z "$BACKEND_PID" ]; then
    echo "🛑 Stopping backend..."
    kill $BACKEND_PID
fi
