"""
Definition of views.
"""
import json
import logging
import requests

from datetime import datetime, date, time, timedelta

from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils.html import strip_tags


#chiamata alle api UP
def getTokenUP(request): # pragma: no cover
    if request.session.get('up_token'):
        return request.session.get('up_token')
    try:
        data = {
            "username": settings.UTENTE_API_UP,
            "password": settings.PASSWORD_API_UP,
            "realm": settings.KEY_API_UP
        }
        url = settings.URL_UP_API +'utenti/login'
        response = requests.post(url, data)

        if response.status_code == 200:
            data = response.json()
            if data.get('id'):
                request.session['up_token'] = data['id']
                return data['id']
        return ""
    except Exception as e:
        print(e)
        return ""


def getData(request, url, cds_cod, body): # pragma: no cover
    try:
        payload = ""
        headers = {
            "Authorization": getTokenUP(request),
            "Content-Type": "application/json",
        }
        payload= json.dumps(body)
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            data = response.json()
            print(data['error']['message'])
            return ""
    except Exception as e:
        print(e)
        return ""


def getEventi(request, aa, cds_cod): # pragma: no cover
    url = settings.URL_UP_API +'Eventi/getEventiByCorso'
    body = {
        "codCorso": cds_cod,
        "annoAccademico": aa,
    }
    return getData(request, url, cds_cod, body)


def getImpegni(request, aa, cds_cod): # pragma: no cover
    url = settings.URL_UP_API + 'Impegni/getImpegniByAnnoAccademico'
    body = {
        "annoAccademico": aa,
        "codCorso": cds_cod,
        "stati": ["P"],
    }
    return getData(request, url, cds_cod, body)
