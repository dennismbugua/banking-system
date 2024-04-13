#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Run collectstatic without interactive prompting
python3.9 manage.py collectstatic --noinput
