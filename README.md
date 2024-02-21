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
 - Upload the data to a bucket: 
```
python3 create_bucket_upload_file.py
```
