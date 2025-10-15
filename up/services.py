"""
Definition of views.
"""

import calendar
import json
import logging
from datetime import datetime

import requests
import zoneinfo
from django.conf import settings

logger = logging.getLogger(__name__)


# chiamata alle api UP
def getUPToken(request):  # pragma: no cover
    if request.session.get('up_token'):
        return request.session.get('up_token')
    try:
        data = {
            "username": settings.UTENTE_API_UP,
            "password": settings.PASSWORD_API_UP,
            "realm": settings.KEY_API_UP,
        }
        url = settings.URL_UP_API + "utenti/login"
        response = requests.post(url, data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("id"):
                request.session["up_token"] = data["id"]
                return data["id"]
        else:
            logger.info(
                f"Error getting UP token: {response.json()['error']['message']}"
            )
    except Exception as e:
        logger.info(f"Error getting UP token: {e}")
    return ""


def getData(request, url, cds_cod, body):  # pragma: no cover
    try:
        headers = {
            "Authorization": getUPToken(request),
            "Content-Type": "application/json",
        }
        payload = json.dumps(body)
        response = requests.post(url, headers=headers, data=payload, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            logger.info(
                f"Error calling UP url {url}: {response.json()['error']['message']}"
            )
    except requests.exceptions.Timeout:
        logger.info(f"UP API {url} timeout")
    except requests.exceptions.ConnectionError:
                logger.info(f"API {url} connection error")
    except Exception as e:
        logger.error(f"Error calling UP url {url}: {e}")
    return []


def getUPImpegni(
    request,
    cds_cod,
    aa,
    year=1,
    date_month="",
    date_year="",
    types=[],
    af_cod="",
    filter_by_af_cod=True,
):  # pragma: no cover
    # filter_by_af_cod: UP non ritorna risultati se si filtrano gli esami per codAF
    url = settings.URL_UP_API + "Impegni/getImpegniByAnnoAccademico"

    try:
        aa = int(aa)
        year = int(year)
    except Exception:
        return []

    settings_tz = zoneinfo.ZoneInfo(settings.TIME_ZONE)
    start_up = ""
    end_up = ""

    if date_month and date_year:
        try:
            up_month = int(date_month)
            up_year = int(date_year)
        except Exception:
            return []

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
        "dataFine": end_up,
        # ~ "codAF": af_cod
        # ~ if filter_by_af_cod
        # ~ else "",
        # UP non ritorna risultati se si filtrano gli esami per codAF
        # Edit: non più vero!
    }

    if af_cod:
        body["codAF"] = af_cod

    return getData(request, url, cds_cod, body)
