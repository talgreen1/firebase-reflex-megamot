# Firebase Students Uploader

This project includes a Python script to upload student data from a CSV file to a Firebase Firestore collection.

## Script: `upload_students_to_firebase.py`

### Usage

Run the script from the command line:

```
python upload_students_to_firebase.py <path_to_csv> [--collection <collection_name>] [--override]
```

#### Arguments
- `<path_to_csv>`: Path to the CSV file (required)
- `--collection <collection_name>`: Name of the Firebase collection (optional, default: `Students`)
- `--override`: If set, will override the collection if it already exists (optional)

#### Examples
- Basic usage (default collection, no override):
  ```
  python upload_students_to_firebase.py csvs/UUStudents.csv
  ```
- Specify collection:
  ```
  python upload_students_to_firebase.py csvs/UUStudents.csv --collection MyCollection
  ```
- Override existing collection:
  ```
  python upload_students_to_firebase.py csvs/UUStudents.csv --override
  ```
- Specify collection and override:
  ```
  python upload_students_to_firebase.py csvs/UUStudents.csv --collection MyCollection --override
  ```

### CSV Schema
The CSV file must have the following columns (in order):

```
id,first_name,last_name,subj_1,subj_2
```

If the schema does not match, the script will print a detailed error and exit.

### Firebase Setup
- Make sure your Firebase Admin SDK JSON key is located at `api-keys/api-keysmegamot-402d2-firebase-adminsdk-fbsvc-61c10d0de0.json`.
- The script uses this key to authenticate with Firebase.

### Dependencies
Install required packages with:

```
pip install -r requirements.txt
```

### Functionality
- Validates the CSV schema.
- Uploads data to the specified Firestore collection.
- Handles collection override logic as described above.
