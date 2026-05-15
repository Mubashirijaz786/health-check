import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project root and the health_helper_app directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

for d in [parent_dir, root_dir]:
    if d not in sys.path:
        sys.path.append(d)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# This is the WSGI application that Vercel will use
app = get_wsgi_application()
