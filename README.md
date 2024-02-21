# MLOps_task
This is a repository with a MLOps pipeline for the MLOps course MDS2022-1

Just make sure to follow these steps: 

 - Clone repository:
```
git clone  PATH TO REPO
```
 - Exit conda environment
```
conda deactivate
```
 - Create a Python virtual environment:
```
python3 -m venv env_xgboost
```
- Activate the virtual environment recently created
```
source env_xgboost/bin/activate
```
- Install the requierements
```
pip install -r requirements.txt
```
 - There is a script to upload the data to a GCP bucket: make sure to change the name of the project_id to your own project's id in the section "Usage". See below. So you should modify the 'create_bucket_upload_file.py like this:
```
# Usage
PROJECT_ID = 'YOUR PROJECT NAME GOES HERE'
BUCKET_NAME = 'mds_bucket_for_data_mlops'
LOCAL_FILE_PATH = 'spotify_data.csv'  # Path to your local file
DESTINATION_PATH = 'data'  # Destination path in the bucket without timestamp
```
- Then you are ready to upload the data to a bucket. 
```
python3 create_bucket_upload_file.py
```
- Once you run the previous script, you will find a message in your console with the path to your bucket, it should look like "the datafile is stored in gs://mds_bucket_for_data_mlops/data_20240221232458/spotify_data.csv"
- Copy this path at the end of the pipeline_template.py file (creo que puedo automatizar esto). 
