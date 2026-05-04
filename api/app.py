import os
import sys

# Add the 'api' directory to the Python path so Vercel can find our local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes import register_routes

# Vercel runs app.py from inside the "api" folder.
# We need to explicitly tell Flask where our "templates" and "static" folders are.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

# Secret key is needed to use flash messages securely
app.secret_key = 'super_secret_beginner_key'

# Register our routes safely
register_routes(app)

# Vercel imports 'app' directly. It doesn't use the block below.
if __name__ == '__main__':
    # Start the application in debug mode for easier development locally
    app.run(debug=True, port=5000)
