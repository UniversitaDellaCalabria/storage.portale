import requests
import json

from .. utils.settings import *

def get_topics_per_page():
    head = {'Authorization': 'Token {}'.format(UNICMS_AUTH_TOKEN)}
    try:
        response = requests.get(UNICMS_TOPIC_API_URL, headers=head, timeout=(10, 10))
        if response.status_code == 200:
            json_response = json.loads(response._content)
            return (response.status_code, json_response)
        else:
            return (response.status_code, {})
    except requests.exceptions.RequestException: 
        return (500, {})