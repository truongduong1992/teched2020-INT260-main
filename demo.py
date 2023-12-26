from sap.aibus.dar.client.data_manager_client import DataManagerClient
import json
import os
from pprint import pprint # for nicer output formatting
from sap.aibus.dar.client.model_manager_client import ModelManagerClient
from sap.aibus.dar.client.exceptions import DARHTTPException
from sap.aibus.dar.client.inference_client import InferenceClient


if not os.path.exists("default_key.json"):
    msg = "key.json is not found. Please follow instructions above to create a service key of"
    msg += " Data Attribute Recommendation. Then, upload it into the same directory where"
    msg += " this notebook is saved."
    print(msg)
    raise ValueError(msg)

with open("default_key.json") as file_handle:
    key = file_handle.read()
    SERVICE_KEY = json.loads(key)
dataset_schema = {
    "features": [
        {"label": "manufacturer", "type": "CATEGORY"},
        {"label": "description", "type": "TEXT"},
        {"label": "price", "type": "NUMBER"}
    ],
    "labels": [
        {"label": "level1_category", "type": "CATEGORY"},
        {"label": "level2_category", "type": "CATEGORY"},
        {"label": "level3_category", "type": "CATEGORY"}
    ],
    "name": "bestbuy-category-prediction",
}
print(SERVICE_KEY)
print(type(SERVICE_KEY))
data_manager = DataManagerClient.construct_from_service_key(SERVICE_KEY)
print(data_manager)
response = data_manager.create_dataset_schema(dataset_schema)
dataset_schema_id = response["id"]

print()
print("DatasetSchema created:")

pprint(response)

print()
print(f"DatasetSchema ID: {dataset_schema_id}")

dataset_resource = data_manager.create_dataset("my-bestbuy-dataset", dataset_schema_id)
dataset_id = dataset_resource["id"]

print()
print("Dataset created:")

pprint(dataset_resource)

print()
print(f"Dataset ID: {dataset_id}")

# Open in binary mode.
with open('bestBuy.csv.gz', 'rb') as file_handle:
    dataset_resource = data_manager.upload_data_to_dataset(dataset_id, file_handle)

print()
print("Dataset after data upload:")
print()
pprint(dataset_resource)
print("processing")
dataset_resource = data_manager.wait_for_dataset_validation(dataset_id)

print()
print("Dataset after validation has finished:")

print()
pprint(dataset_resource)

model_manager = ModelManagerClient.construct_from_service_key(SERVICE_KEY)

model_template_id = "d7810207-ca31-4d4d-9b5a-841a644fd81f" # hierarchical template
model_name = "bestbuy-hierarchy-model"

job_resource = model_manager.create_job(model_name, dataset_id, model_template_id)
job_id = job_resource['id']

print()
print("Job resource:")
print()

pprint(job_resource)

print()
print(f"ID of submitted Job: {job_id}")
job_resource = model_manager.wait_for_job(job_id)

print()

print("Job resource after training is finished:")

pprint(job_resource)
model_resource = model_manager.read_model_by_name(model_name)

print()
pprint(model_resource)

deployment_resource =  model_manager.create_deployment(model_name)
deployment_id = deployment_resource["id"]

print()
print("Deployment resource:")
print()

pprint(deployment_resource)

print(f"Deployment ID: {deployment_id}")

deployment_resource = model_manager.wait_for_deployment(deployment_id)

print()
print("Finished deployment resource:")
print()

pprint(deployment_resource)

##Executing Inference requests
inference = InferenceClient.construct_from_service_key(SERVICE_KEY)

objects_to_be_classified = [
    {
        "features": [
            {"name": "manufacturer", "value": "Energizer"},
            {"name": "description", "value": "Alkaline batteries; 1.5V"},
            {"name": "price", "value":  "5.99"},
        ],
    },
]

inference_response = inference.create_inference_request(model_name, objects_to_be_classified)

print()
print("Inference request processed. Response:")
print()
pprint(inference_response)
my_own_items = [
    {
        "features": [
            {"name": "manufacturer", "value": "EDIT THIS"},
            {"name": "description", "value": "EDIT THIS"},
            {"name": "price", "value":  "0.00"},
        ],
    },
]

inference_response = inference.create_inference_request(model_name, my_own_items)

print()
print("Inference request processed. Response:")
print()
pprint(inference_response)
objects_to_be_classified = [
    {
        "objectId": "optional-identifier-1",
        "features": [
            {"name": "manufacturer", "value": "Energizer"},
            {"name": "description", "value": "Alkaline batteries; 1.5V"},
            {"name": "price", "value":  "5.99"},
        ],
    },
    {
        "objectId": "optional-identifier-2",
        "features": [
            {"name": "manufacturer", "value": "Eidos"},
            {"name": "description", "value": "Unravel a grim conspiracy at the brink of Revolution"},
            {"name": "price", "value":  "19.99"},
        ],
    },
    {
        "objectId": "optional-identifier-3",
        "features": [
            {"name": "manufacturer", "value": "Cadac"},
            {"name": "description", "value": "CADAC Grill Plate for Safari Chef Grills: 12\""
                                             + "cooking surface; designed for use with Safari Chef grills;"
                                             + "105 sq. in. cooking surface; PTFE nonstick coating;"
                                             + " 2 grill surfaces"
            },
            {"name": "price", "value":  "39.99"},
        ],
    }
]


inference_response = inference.create_inference_request(model_name, objects_to_be_classified, top_n=3)

print()
print("Inference request processed. Response:")
print()
pprint(inference_response)
# Inspect all video games with just a top-level category entry
video_games = df[df['level1_category'] == 'Video Games']
video_games.loc[df['level2_category'].isna() & df['level3_category'].isna()].head(5)


##Cleanup
# Clean up all resources created earlier

CLEANUP_SESSION = False

def cleanup_session():
     model_manager.delete_deployment_by_id(deployment_id) # this can take a few seconds
     model_manager.delete_model_by_name(model_name)
     model_manager.delete_job_by_id(job_id)

     data_manager.delete_dataset_by_id(dataset_id)
     data_manager.delete_dataset_schema_by_id(dataset_schema_id)
     print("DONE cleaning up!")

 if CLEANUP_SESSION:
     print("Cleaning up resources generated in this session.")
     cleanup_session()
 else:
     print("Not cleaning up. Set 'CLEANUP_SESSION = True' above and run again!")
    
