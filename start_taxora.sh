#!/bin/bash

echo "========================================"
echo "   Taxora - AI Finance Assistant"
echo "   Starting Application..."
echo "========================================"
echo

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

python3 --version

echo
echo "Setting up backend..."
cd backend

echo "Installing backend dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install backend dependencies"
    exit 1
fi

echo
echo "Checking environment configuration..."
if [ ! -f .env ]; then
    echo "WARNING: .env file not found. Copying from .env.example"
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit backend/.env with your IBM Watson API keys"
    echo "Press Enter to continue after configuring your API keys..."
    read
fi

echo
echo "Starting backend server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 5

cd ../frontend

echo
echo "Installing frontend dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install frontend dependencies"
    kill $BACKEND_PID
    exit 1
fi

echo
echo "Starting frontend application..."
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!

echo
echo "========================================"
echo "   Taxora is now running!"
echo "========================================"
echo
echo "Backend API: http://localhost:8000"
echo "Frontend App: http://localhost:8501"
echo "API Docs: http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop both services"
echo

# Wait for user interrupt
trap 'echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
