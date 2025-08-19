"""
WSGI config for banking_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# WHY: Set the default settings module for Django
# This tells Django which settings file to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

# WHY: Create the WSGI application object
# This is what web servers use to communicate with Django
application = get_wsgi_application()

# WHY: Alias for Vercel deployment compatibility
# Some deployment platforms expect 'app' instead of 'application'
app = application