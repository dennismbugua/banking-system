#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Run Django collectstatic command to gather static files
python3.9 manage.py collectstatic --noinput

# Ensure the output directory exists
mkdir -p staticfiles

# Move collected static files to the output directory
mv staticfiles/* staticfiles/
