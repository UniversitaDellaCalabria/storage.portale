import base64
import logging
import requests

from django.conf import settings


logger = logging.getLogger(__name__)


# chiamata alle api Esse3
def getEsse3Token(request):  # pragma: no cover
    if request.session.get('esse3_token'):
        return request.session.get('esse3_token')
    try:
        _upseq = ':'.join((settings.UTENTE_API_ESSE3, settings.PASSWORD_API_ESSE3))
        token = base64.b64encode(_upseq.encode('utf-8')).decode()
        request.session['esse3_token'] = token
        return token
    except Exception as e:
        logger.error(f"Error getting Esse3 token: {e}")
        return ''


def getEsse3Appelli(request, cds_id, af_id, aa):  # pragma: no cover
    headers = {'Authorization': f'Basic {getEsse3Token(request)}'}
    url = f"{settings.URL_ESSE3_API}calesa-service-v1/appelli/{cds_id}/{af_id}/?minDataApp=01/01/{ aa }"
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        return response.json()
    logger.error(f"Error calling Esse3 API {url}: {response.json()['retErrMsg']}")
    return []
