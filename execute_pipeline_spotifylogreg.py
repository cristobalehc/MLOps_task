from datetime import datetime
from google.cloud import aiplatform

if __name__ == '__main__':
    TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")

    #Crear el job. 
    job = aiplatform.PipelineJob(
        display_name="spotify-mode-prediction-logistic",  # Updated display name
        template_path="spotify_mode_prediction_pipeline_logistic_regression.json",  # Updated to your new pipeline JSON file
        job_id="spotify-mode-prediction-{0}".format(TIMESTAMP),  # Updated job ID
        enable_caching=False  # Set to False if you want to disable caching for testing
    )

    job.submit()

    print('Spotify mode prediction pipeline successfully submitted')
