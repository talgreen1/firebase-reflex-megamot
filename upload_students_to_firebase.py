import argparse
import csv
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore

# Constants
REQUIRED_SCHEMA = ['id', 'first_name', 'last_name', 'subj_1', 'subj_2']
DEFAULT_COLLECTION = 'Students'
FIREBASE_CRED_PATH = os.path.join('api-keys', 'api-keysmegamot-402d2-firebase-adminsdk-fbsvc-61c10d0de0.json')

def parse_args():
    parser = argparse.ArgumentParser(description='Upload students CSV to Firebase Firestore.')
    parser.add_argument('csv_path', help='Path to the CSV file')
    parser.add_argument('--collection', default=DEFAULT_COLLECTION, help='Firebase collection name (default: Students)')
    parser.add_argument('--override', action='store_true', help='Override collection if it exists')
    return parser.parse_args()

def validate_csv_schema(csv_path):
    with open(csv_path, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except Exception as e:
            print(f'Error reading CSV header: {e}')
            sys.exit(1)
        if header != REQUIRED_SCHEMA:
            print(f'CSV schema mismatch.\nExpected: {REQUIRED_SCHEMA}\nFound:    {header}')
            sys.exit(1)

def read_csv_data(csv_path):
    with open(csv_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def collection_exists(db, collection_name):
    docs = db.collection(collection_name).limit(1).get()
    return len(docs) > 0

def clear_collection(db, collection_name):
    docs = db.collection(collection_name).stream()
    for doc in docs:
        doc.reference.delete()

def upload_to_firestore(db, collection_name, data):
    for row in data:
        doc_id = row['id']
        db.collection(collection_name).document(doc_id).set(row)

def main():
    args = parse_args()
    csv_path = args.csv_path
    collection_name = args.collection
    override = args.override

    # 1. Validate CSV path and schema
    if not os.path.isfile(csv_path):
        print(f'File not found: {csv_path}')
        sys.exit(1)
    validate_csv_schema(csv_path)

    # 2. Read CSV data
    data = read_csv_data(csv_path)

    # 3. Init Firebase
    db = init_firebase()

    # 4. Check collection existence
    if collection_exists(db, collection_name):
        if not override:
            print(f"Collection '{collection_name}' already exists. Use --override to overwrite.")
            sys.exit(1)
        else:
            print(f"Overriding collection '{collection_name}'...")
            clear_collection(db, collection_name)
    else:
        print(f"Uploading to new collection '{collection_name}'...")

    # 5. Upload data
    upload_to_firestore(db, collection_name, data)
    print(f"Upload complete. {len(data)} records uploaded to '{collection_name}'.")

if __name__ == '__main__':
    main()

