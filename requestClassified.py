from sap.aibus.dar.client.data_manager_client import DataManagerClient
import json
import os
import pandas as pd
from pprint import pprint # for nicer output formatting
from sap.aibus.dar.client.model_manager_client import ModelManagerClient
from sap.aibus.dar.client.exceptions import DARHTTPException
from sap.aibus.dar.client.inference_client import InferenceClient

model_name = "bestbuy-hierarchy-model"

if not os.path.exists("default_key.json"):
    msg = "default_key.json is not found. Please follow instructions above to create a service key of"
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

