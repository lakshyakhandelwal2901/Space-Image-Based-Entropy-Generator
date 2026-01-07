#!/bin/bash

# Quick start script for Space Entropy Generator

echo "🌌 Space Entropy Generator - Quick Start"
echo "========================================"
echo ""

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
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
fi

# Create image storage directory
mkdir -p /tmp/space_entropy_images

echo ""
echo "✅ Setup complete!"
echo ""
echo "Available commands:"
echo "  python test_ingestion.py    - Test image ingestion"
echo "  python -m app.main          - Run the API server"
echo "  docker-compose up -d        - Run with Docker"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Documentation at: http://localhost:8000/docs"
echo ""
