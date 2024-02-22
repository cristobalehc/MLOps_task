# MLOps pipeline using vertex for MDS2022-1. 

This is a repository with a MLOps pipeline for the MLOps course MDS2022-1. It will create a simple pipeline to train a logistic regression model and predict whether a song has a major or minor mode, based on song characteristics listed on Spotify. It will load and use a spotify dataset. 

**Important note:** This repository assumes that you are logged in your GCP account, and have a running workbench instance with notebooks. 


To try it out, make sure to follow these steps: 

 - Clone repository:
```
git clone https://github.com/cristobalehc/MLOps_task.git
```
 - Exit conda environment
```
conda deactivate
```
 - Create a Python virtual environment:
```
python3 -m venv spotifylogreg_venv
```
- Activate the virtual environment recently created
```
source spotifylogreg_venv/bin/activate
```
- Install the requierements
```
pip install -r requirements.txt
```
 - Modify the 'create_bucket_upload_file.py' file: There is a script to upload the data to a GCP bucket: make sure to change the name of the **PPROJECT_ID** in line 30 to your own project's id in the section "Usage". See below. So you should modify the 'create_bucket_upload_file.py' like this:
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

- Copy this path at the end of the pipeline_spotify_logreg.py file in -line- 121 as follows. 
```
data_path: str = 'gs://mds_bucket_for_data_mlops/data_20240221224402/spotify_data.csv',
```
- Compile the pipeline with the modified code:
```
python3 pipeline_spotify_logreg.py
```
- It will create a json file with the configuration. To excecute the pipeline run the following code:
```
python3 execute_pipeline_spotifylogreg.py
```

Now you will have to wait a little bit for the pipeline to run. 


## Using the API with the GUI: 

You can try to make an inference with the following payload in the model registry GUI widget:
```
{
  "instances": [
    [2020, 7, 5.1, 120, 0.65, 0.8, 0.1, 0.0, 0.3, 0.2, 0.75]
  ]
}
```
![image](https://github.com/cristobalehc/MLOps_task/assets/87136104/c27400d7-abb8-4784-9758-81a29ee266ef)

