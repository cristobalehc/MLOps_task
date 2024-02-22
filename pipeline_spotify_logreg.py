import kfp
from kfp import dsl
from kfp.v2 import compiler
from kfp.v2.dsl import Artifact, Dataset, Input, InputPath, Model, Output, OutputPath, Metrics, component, pipeline
from google_cloud_pipeline_components import aiplatform as gcc_aip

PROJECT_ID = 'future-abacus-414917'  # Actualizar con ID propio. 

@component(
    packages_to_install=["pandas==1.3.5", "scikit-learn==1.0.2","fsspec", "gcsfs"],
)
def load_and_prepare_data(
    data_path: str, 
    dataset: Output[Dataset],
):
    """Carga y prepara los datos de Spotify desde un archivo CSV."""
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder

    # Cargar datos
    encodings = ['utf-8', 'ISO-8859-1', 'latin1']  # Probar diferents encodings. 
    for encoding in encodings:
        try:
            spotify_data = pd.read_csv(data_path, encoding=encoding)
            print(f"File read successfully with {encoding} encoding.")
            break  # Salir del loop si funciona. 
        except UnicodeDecodeError as e:
            print(f"Failed to read with {encoding}: {e}")
            if encoding == encodings[-1]:  # Si no funciona levantar error. 
                raise UnicodeDecodeError(f"Failed to read file with tried encodings: {encodings}")

    # Seleccionar columnas relevantes y codificar la variable objetivo
    features = [
        'released_year', 'released_month', 'listas_spotify_log', 'bpm', 
        'porcentaje_bailable', 'porcentaje_energia', 'porcentaje_acustica', 
        'porcentaje_instrumental', 'porcentaje_voz', 'porcentaje_envivo', 'valencia'
    ]
    target = 'modo'
    spotify_data = spotify_data[features + [target]]
    
    le = LabelEncoder()
    spotify_data[target] = le.fit_transform(spotify_data[target])
    
    # Guardar los datos preprocesados en un archivo CSV temporal
    spotify_data.to_csv(dataset.path, index=False)
    
    
@component(
    packages_to_install=["scikit-learn==1.0.2", "pandas==1.3.5", "joblib==1.1.0"],
)
def logistic_regression_training(
    dataset: Input[Dataset],
    model_output: Output[Model],
    metrics: Output[Metrics],
):
    import os
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, roc_auc_score, recall_score, precision_score
    from sklearn.model_selection import train_test_split
    import joblib

    # Load data.  
    spotify_data = pd.read_csv(dataset.path)
    X = spotify_data.drop('modo', axis=1)
    y = spotify_data['modo']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the logistic regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    auc = roc_auc_score(y_test, predictions)
    recall = recall_score(y_test, predictions, average='binary')
    precision = precision_score(y_test, predictions, average='binary')

    # Log metrics
    metrics.log_metric("accuracy", accuracy * 100.0)
    metrics.log_metric("AUC", auc)
    metrics.log_metric("recall", recall)
    metrics.log_metric("precision", precision)

    # Save the trained model
    os.makedirs(model_output.path, exist_ok=True)
    joblib.dump(model, os.path.join(model_output.path, "model.joblib"))

@component(
    packages_to_install=["google-cloud-aiplatform==1.25.0"],
)
def deploy_model(
    model: Input[Model],
    project_id: str,
    vertex_endpoint: Output[Artifact],
    vertex_model: Output[Model],
):
    from google.cloud import aiplatform

    aiplatform.init(project=project_id)

    deployed_model = aiplatform.Model.upload(
        display_name="spotify-mode-prediction-model-logistic-regression",
        artifact_uri=model.uri,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-23:latest",
    )
    endpoint = deployed_model.deploy(machine_type="n1-standard-4")

    vertex_endpoint.uri = endpoint.resource_name
    vertex_model.uri = deployed_model.resource_name

@dsl.pipeline(
    name="spotify-mode-prediction-pipeline-logistic-regression",
    description="A pipeline to train and deploy a Spotify mode prediction model using Logistic Regression.",
)
def spotify_pipeline(
    data_path: str = 'gs://mds_bucket_for_data_mlops/data_20240221224402/spotify_data.csv',
):
    prepare_data_task = load_and_prepare_data(data_path=data_path)
    training_task = logistic_regression_training(
        dataset=prepare_data_task.outputs["dataset"],
    )
    deploy_model(
        model=training_task.outputs["model_output"],
        project_id=PROJECT_ID,
    )

if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=spotify_pipeline, 
        package_path="spotify_mode_prediction_pipeline_logistic_regression.json"
    ) 