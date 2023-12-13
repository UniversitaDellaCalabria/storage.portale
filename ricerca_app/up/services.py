"""
Definition of views.
"""
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
        response = requests.post(url, data, timeout=5)

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
        response = requests.post(url, headers=headers, data=payload, timeout=5)
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


def getImpegni(request, cds_cod, aa, year=1, date_month=None, date_year=None, types=[], af_cod=None): # pragma: no cover
    url = settings.URL_UP_API + 'Impegni/getImpegniByAnnoAccademico'

    settings_tz = zoneinfo.ZoneInfo(settings.TIME_ZONE)

    start_up = ""
    end_up = ""

    try:
        aa = int(aa)
        year = int(year)
    except:
        return ""

    if date_month and date_year:
        try:
            up_month = int(date_month)
            up_year = int(date_year)
        except:
            return ""

        last_day = calendar.monthrange(up_year, up_month)[1]

        start = datetime(up_year, up_month, 1, 00, 00, tzinfo=settings_tz)
        end = datetime(up_year, up_month, last_day, 23, 59, tzinfo=settings_tz)

        start_up = datetime.strftime(start, "%Y-%m-%dT%H:%M:00.000Z")
        end_up = datetime.strftime(end, "%Y-%m-%dT%H:%M:00.000Z")

    body = {
        "annoAccademico": aa,
        "annoCorso": year,
        "codCorso": cds_cod,
        "stati": ["P"],
        "codTipiEvento": types,
        "dataInizio": start_up,
        "dataFine": end_up
    }
    return getData(request, url, cds_cod, body)
