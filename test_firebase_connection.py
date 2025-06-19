import firebase_admin
from firebase_admin import credentials, firestore
import os

# Path to your service account key
SERVICE_ACCOUNT_PATH = os.path.join(
    os.path.dirname(__file__), 'api-keys', 'api-keysmegamot-402d2-firebase-adminsdk-fbsvc-61c10d0de0.json')

try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    # Try to fetch collections as a test
    collections = list(db.collections())
    print(f"Successfully connected to Firebase! Found {len(collections)} collections.")
except Exception as e:
    print(f"Failed to connect to Firebase: {e}")

