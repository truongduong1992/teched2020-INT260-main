import json
import os

if not os.path.exists("key.json"):
    msg = "key.json is not found. Please follow instructions above to create a service key of"
    msg += " Data Attribute Recommendation. Then, upload it into the same directory where"
    msg += " this notebook is saved."
    print(msg)
    raise ValueError(msg)

with open("key.json") as file_handle:
    key = file_handle.read()
    SERVICE_KEY = json.loads(key)

CLEANUP_EVERYTHING = False

def cleanup_everything():
    import logging
    import sys

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    import json
    import os

    if not os.path.exists("key.json"):
        msg = "key.json is not found. Please follow instructions above to create a service key of"
        msg += " Data Attribute Recommendation. Then, upload it into the same directory where"
        msg += " this notebook is saved."
        print(msg)
        raise ValueError(msg)

    with open("key.json") as file_handle:
        key = file_handle.read()
        SERVICE_KEY = json.loads(key)

    from sap.aibus.dar.client.model_manager_client import ModelManagerClient

    model_manager = ModelManagerClient.construct_from_service_key(SERVICE_KEY)

    for deployment in model_manager.read_deployment_collection()["deployments"]:
        model_manager.delete_deployment_by_id(deployment["id"])

    for model in model_manager.read_model_collection()["models"]:
        model_manager.delete_model_by_name(model["name"])

    for job in model_manager.read_job_collection()["jobs"]:
        model_manager.delete_job_by_id(job["id"])

    from sap.aibus.dar.client.data_manager_client import DataManagerClient

    data_manager = DataManagerClient.construct_from_service_key(SERVICE_KEY)

    for dataset in data_manager.read_dataset_collection()["datasets"]:
        data_manager.delete_dataset_by_id(dataset["id"])

    for dataset_schema in data_manager.read_dataset_schema_collection()["datasetSchemas"]:
        data_manager.delete_dataset_schema_by_id(dataset_schema["id"])
        
    print("Cleanup done!")

if CLEANUP_EVERYTHING:
    print("Cleaning up all resources in this service instance.")
    cleanup_everything()
else:
    print("Not cleaning up. Set 'CLEANUP_EVERYTHING = True' above and run again.")
