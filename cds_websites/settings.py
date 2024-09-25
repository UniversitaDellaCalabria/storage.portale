from django.conf import settings

OFFICE_CDS_WEBSITES = getattr(settings, 'OFFICE_CDS_WEBSITES', 'cds_websites')
OFFICE_CDS_WEBSITES_STRUCTURES = getattr(settings, 'OFFICE_CDS_WEBSITES_STRUCTURES', 'cds_websites_structures')

UNICMS_TOPIC_API_URL = getattr(settings, 'UNICMS_TOPIC_API_URL', '')
UNICMS_ROOT_URL = getattr(settings, 'UNICMS_ROOT_URL', '')
UNICMS_PUBLICATION_API_URL = getattr(settings, 'UNICMS_PUBLICATION_API_URL', '')
UNICMS_WEBPATH_API_URL = getattr(settings, 'UNICMS_WEBPATH_API_URL', '')
UNICMS_OBJECT_API = getattr(settings, 'UNICMS_OBJECT_API', {})

UNICMS_CORSI_BASE_URL = getattr(settings, 'UNICMS_CORSI_BASE_URL', '')
UNICMS_CORSI_LM_URL = getattr(settings, 'UNICMS_CORSI_LM_URL', UNICMS_CORSI_BASE_URL + '/lm')
UNICMS_CORSI_LT_LMCU_URL = getattr(settings, 'UNICMS_CORSI_LT_LMCU_URL', UNICMS_CORSI_BASE_URL + '/lt-lmcu')