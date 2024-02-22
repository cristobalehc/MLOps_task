from google.cloud import storage
from datetime import datetime

def create_bucket_and_upload_file(project_id, bucket_name, source_file_path, file_destination_path):
    """Creates a bucket (if it doesn't exist), creates a timestamped folder, and uploads a file to it."""
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)

    # Create the bucket if it does not exist
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket, location="us-central1")  # Choose your bucket location if needed
        print(f"Bucket {bucket_name} created.")

    # Generate timestamped folder name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    timestamped_folder = f"{file_destination_path}_{timestamp}"

    # Full path for file upload
    full_blob_name = f"{timestamped_folder}/{source_file_path.split('/')[-1]}"

    # Upload the file
    blob = bucket.blob(full_blob_name)
    blob.upload_from_filename(source_file_path)
    print(f"File {source_file_path} uploaded to {full_blob_name}.")
    
    print(f"the datafile is stored in gs://{BUCKET_NAME}/{full_blob_name}")
    return full_blob_name  # Return the path where the file was uploaded

# Usage
PROJECT_ID = 'future-abacus-414917'
BUCKET_NAME = 'mds_bucket_for_data_mlops'
LOCAL_FILE_PATH = 'spotify_data.csv'  # Path to your local file
DESTINATION_PATH = 'data'  # Destination path in the bucket without timestamp

# This will create the bucket and upload the file to the timestamped folder
uploaded_file_path = create_bucket_and_upload_file(PROJECT_ID, BUCKET_NAME, LOCAL_FILE_PATH, DESTINATION_PATH)


