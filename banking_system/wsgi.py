"""
WSGI config for banking_system project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

# Get WSGI application
application = get_wsgi_application()

# Alias for Vercel compatibility
app = application

# Collect static files on first import (for Vercel)
if os.environ.get('VERCEL_ENV'):
    try:
        import django
        from django.core.management import call_command
        django.setup()
        call_command('collectstatic', '--noinput', verbosity=0)
    except Exception as e:
        print(f"Static files collection failed: {e}")
        pass