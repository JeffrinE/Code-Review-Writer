import requests
import json
url = "http://localhost:11434/api/tags"


def get_local_models():
    try:
        local_models_bytes = requests.get(url)
        model_list = []
        local_models = local_models_bytes.json()["models"]
        for model in local_models:
            model_list.append(model["name"])
        return model_list
    except:
        return None