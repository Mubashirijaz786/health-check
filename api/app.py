import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root to the Python path
# This file is in health_helper_app/api/app.py, so the root is one level up
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# This is the WSGI application that Vercel will use
app = get_wsgi_application()
