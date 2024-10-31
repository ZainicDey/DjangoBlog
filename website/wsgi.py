import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')  # Update 'website' to your project name
application = get_wsgi_application()
