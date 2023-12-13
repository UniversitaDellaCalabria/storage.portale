"""
Definition of views.
"""
import base64
import calendar
import json
import logging
import requests
import zoneinfo

from datetime import datetime, date, time, timedelta

from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.html import strip_tags


#chiamata alle api Esse3
def getTokenEsse3(): # pragma: no cover
    try:
        _upseq = ':'.join((settings.UTENTE_API_ESSE3, settings.PASSWORD_API_ESSE3))
        token = base64.b64encode(_upseq.encode('utf-8')).decode()
        return token
    except Exception as e:
        print(e)
        return ""


def getAppelli(request, cds_id, af_id, aa): # pragma: no cover
    headers = {'Authorization': f'Basic {getTokenEsse3()}'}

    url = f"{settings.URL_ESSE3_API}calesa-service-v1/appelli/{cds_id}/{af_id}/?aaCalId={aa}"
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        return response.json()
    return ""
