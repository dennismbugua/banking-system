#!/bin/bash

echo "Starting build process..."

# Install Python dependencies with better error handling
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
# Run Django collectstatic command to gather static files
python manage.py collectstatic --noinput --clear

# Ensure the output directory exists
mkdir -p staticfiles

# Move collected static files to the output directory
mv staticfiles/* staticfiles/
