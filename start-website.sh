#!/bin/bash
# Quick start script for the Entropy.Space website

set -e

WEBSITE_DIR="website/solar-entropy-api-main/solar-entropy-api-main"

echo "🚀 Starting Entropy.Space Website..."
echo ""

# Check if we're in the right directory
if [ ! -d "$WEBSITE_DIR" ]; then
    echo "❌ Error: Website directory not found at $WEBSITE_DIR"
    echo "Please run this script from the project root directory."
    exit 1
fi

cd "$WEBSITE_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creating .env.local from .env.example..."
    cp .env.example .env.local
    echo "✅ Created .env.local - edit this file to configure your API base URL"
    echo ""
fi

# Start the dev server
echo "🌐 Starting development server on http://localhost:8080..."
echo "   Backend API expected at: http://localhost:8000/api/v1"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
