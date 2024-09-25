import json

import requests
from cds_websites.settings import UNICMS_TOPIC_API_URL
from generics.settings import UNICMS_AUTH_TOKEN


def get_topics_per_page():
    head = {"Authorization": "Token {}".format(UNICMS_AUTH_TOKEN)}
    res = {"status_code": 500, "content": {}}
    try:
        response = requests.get(UNICMS_TOPIC_API_URL, headers=head, timeout=(10, 10))
        res["status_code"] = response.status_code
        if response.status_code == 200:
            json_response = json.loads(response._content)
            res["content"] = json_response
        return res
    except requests.exceptions.RequestException:
        return res

