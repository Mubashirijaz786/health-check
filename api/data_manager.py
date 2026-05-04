import json
import os
import uuid
from datetime import datetime

# Vercel has a read-only file system. If we want to save data, we must use /tmp.
# However, /tmp data is lost when Vercel restarts the app container.
# For production, a real database should be used.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'):
    DATA_FILE = '/tmp/data.json'
else:
    DATA_FILE = os.path.join(base_dir, 'data.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"persons": []}
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            # Migration from old list format to new nested format
            if isinstance(data, list):
                new_data = {
                    "persons": [
                        {
                            "id": str(uuid.uuid4()),
                            "name": "Default User",
                            "medicines": []
                        }
                    ]
                }
                for med in data:
                    new_data["persons"][0]["medicines"].append({
                        "id": med.get("id", str(uuid.uuid4())),
                        "name": med.get("name", ""),
                        "dosage": med.get("dosage", ""),
                        "times": [med.get("time", "08:00")] if "time" in med else med.get("times", []),
                        "total_days": 30,
                        "start_date": datetime.now().strftime("%Y-%m-%d")
                    })
                save_data(new_data)
                return new_data
            return data
    except Exception:
        return {"persons": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
