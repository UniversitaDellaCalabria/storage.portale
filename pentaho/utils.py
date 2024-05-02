import logging
import requests
import base64
import os

from django.conf import settings

from . settings import *

# from xlsx2html import xlsx2html

logger = logging.getLogger(__name__)


PENTAHO_BASE = getattr(settings, "PENTAHO_BASE", PENTAHO_BASE)
PENTAHO_ISODID_MEDIA_PATH = getattr(settings, "PENTAHO_ISODID_MEDIA_PATH", PENTAHO_ISODID_MEDIA_PATH)
PENTAHO_ISODID_REPORT_OUTPUT = getattr(settings, "PENTAHO_ISODID_REPORT_OUTPUT", PENTAHO_ISODID_REPORT_OUTPUT)
PENTAHO_ISODID_REPORT_PARAMS = getattr(settings, "PENTAHO_ISODID_REPORT_PARAMS", PENTAHO_ISODID_REPORT_PARAMS)
PENTAHO_ISODID_REPORT_PATH = getattr(settings, "PENTAHO_ISODID_REPORT_PATH", PENTAHO_ISODID_REPORT_PATH)
PENTAHO_USERNAME = getattr(settings, "PENTAHO_USERNAME", PENTAHO_USERNAME)
PENTAHO_PASSWORD = getattr(settings, "PENTAHO_PASSWORD", PENTAHO_PASSWORD)

_upseq = f"{PENTAHO_USERNAME}:{PENTAHO_PASSWORD}"
token = base64.b64encode(_upseq.encode('utf-8')).decode()
headers = {'Authorization': f'Basic {token}'}


def getIsodidReport(cds=[], years=[]):
    for year in years:
        for cds_cod in cds:
            params = PENTAHO_ISODID_REPORT_PARAMS.format(year, year, cds_cod)
            url = f"{PENTAHO_BASE}/{PENTAHO_ISODID_REPORT_PATH}/report?renderMode=REPORT&locale=it_IT&output-target={PENTAHO_ISODID_REPORT_OUTPUT}{params}"
            # chiama Pentaho
            filename = f"{PENTAHO_ISODID_MEDIA_PATH}/{year}/{cds_cod}.csv"
            try:
                response = requests.get(url, headers=headers, timeout=7000)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                f = open(filename, "wb")
                f.write(response.content)
                f.close()
                logger.error(f"Pentaho ISODID report for {year} - {cds_cod} : OK")
            except Exception as e:
                logger.error(e)
