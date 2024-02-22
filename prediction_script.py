from typing import Dict, List, Union

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

### Modified google function:

def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    Send a prediction request to a deployed model on Vertex AI.

    Args:
        project (str): Project where the AI Platform Model is deployed.
        endpoint_id (str): Endpoint ID of the model.
        instances (Union[Dict, List[Dict]]): Instances to predict.
        location (str, optional): The location of the AI Platform Model. Defaults to 'us-central1'.
        api_endpoint (str, optional): The AI Platform API endpoint. Defaults to 'us-central1-aiplatform.googleapis.com'.
    """
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]

    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )

    response = client.predict(
        endpoint=endpoint, instances=instances
    )

    print("Model Response:")
    print(" deployed_model_id:", response.deployed_model_id)
    
    predictions = response.predictions
    for prediction in predictions:
        if prediction == 0:
            print('The mode of the song is Major: is it happy?')
        elif prediction == 1:
            print('The mode of the song is Minor: is it sad?')
        else:
            print("Unexpected prediction:", prediction)

#### Function call for prediction making. 

predict_custom_trained_model_sample(
    project="461824224196",
    endpoint_id="1905825285865996288",
    instances=[
        [2020, 7, 5.1, 120, 0.65, 0.8, 0.1, 0.0, 0.3, 0.2, 0.75]
    ]
)
