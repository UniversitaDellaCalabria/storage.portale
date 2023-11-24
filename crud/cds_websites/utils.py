import requests
import json

from .. utils.settings import *

def get_topics_per_page():
    head = {'Authorization': 'Token {}'.format(UNICMS_AUTH_TOKEN)}
    res = {
        "status_code": 500,
        "content": {}
    }
    try:
        response = requests.get(UNICMS_TOPIC_API_URL, headers=head, timeout=(10, 10))
        res["status_code"] = response.status_code
        if response.status_code == 200:
            json_response = json.loads(response._content)
            res["content"] = json_response
            return res
        else:
            return res
    except requests.exceptions.RequestException: 
        return res
    
def get_object_preview(obj_id, obj_class) :
    head = {'Authorization': 'Token {}'.format(UNICMS_AUTH_TOKEN)}
    res = {
        "status_code": 500
    }
    try:
        api_url = UNICMS_OBJECT_API[obj_class].format(obj_id)
        response = requests.get(api_url, headers=head, timeout=(10, 10))
        res["status_code"] = response.status_code
        if response.status_code == 200:
            json_response = json.loads(response._content)
            res["object_class"] = obj_class
            if obj_class == "Publication":
                res["content"] = json_response["content"]
                return (response.status_code, res)
            else:
                res["name"] = json_response["name"]
                res["content"] = UNICMS_ROOT_URL + json_response["get_full_path"]
                return res
        else:
            return res
    except requests.exceptions.RequestException: 
        return res