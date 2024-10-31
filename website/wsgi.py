import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'DJANGO_SETTINGS_MODULE' environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  # Replace 'your_project_name' with your actual project name

# Get the WSGI application for your project
application = get_wsgi_application()