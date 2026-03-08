#!/bin/bash

echo "================================"
echo "Portfolio Website Setup"
echo "================================"
echo ""

# Create static directories
echo "Creating directories..."
mkdir -p static/images
mkdir -p static/css
mkdir -p static/js

# Copy images from project folder
echo "Copying challenge images..."
if [ -d "/mnt/project" ]; then
    cp /mnt/project/*.jpg static/images/ 2>/dev/null
    echo "✓ Images copied from /mnt/project"
else
    echo "⚠ /mnt/project not found - please copy images manually to static/images/"
fi

# Install Python dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "================================"
echo "✓ Setup Complete!"
echo "================================"
echo ""
echo "To run the website:"
echo "  python app.py"
echo ""
echo "Then visit: http://localhost:5000"
echo ""
