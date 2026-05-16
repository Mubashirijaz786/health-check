import os
import sys
import shutil
from django.core.wsgi import get_wsgi_application

# Add the project root to the Python path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Handle SQLite database on Vercel (Read-only filesystem)
if os.environ.get('VERCEL'):
    src = os.path.join(path, 'db.sqlite3')
    dst = '/tmp/db.sqlite3'
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Auto-run migrations on Vercel startup
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    from django.db import connection
    try:
        # This will run migrations automatically on the live server
        app = get_wsgi_application()
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")

# This is the WSGI application that Vercel will use
app = get_wsgi_application()
