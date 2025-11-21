"""
WSGI config for api_project project.

It exposes the WSGI callable as a module-level variable named `application`.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module to the correct path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')

application = get_wsgi_application()
