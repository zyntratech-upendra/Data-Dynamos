#!/bin/bash

# SpectraMining AI - Linux/Mac Launcher

echo "🛰️  SpectraMining AI - Starting..."

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "🚀 Starting SpectraMining AI..."
echo "🌐 Open your browser at: http://localhost:5000"
echo ""
python app.py
