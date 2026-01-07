#!/bin/bash

# Space Entropy Generator - Stop Script

echo "🛑 Stopping Space Entropy Generator..."
echo ""

# Stop FastAPI server
echo "1️⃣  Stopping FastAPI server..."
pkill -f "python -m app.main"
if [ $? -eq 0 ]; then
    echo "   ✅ Server stopped"
else
    echo "   ⚠️  No server process found"
fi

# Stop Redis
echo ""
echo "2️⃣  Stopping Redis..."
docker-compose stop redis
if [ $? -eq 0 ]; then
    echo "   ✅ Redis stopped"
else
    echo "   ⚠️  Failed to stop Redis"
fi

echo ""
echo "✅ Shutdown complete"
