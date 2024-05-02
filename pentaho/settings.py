from django.conf import settings


PENTAHO_USERNAME = ""
PENTAHO_PASSWORD = ""

PENTAHO_MEDIA_PATH = f"{settings.MEDIA_URL}pentaho/"

PENTAHO_BASE = "https://repo-unical.bi.u-gov.it/pentaho/api/repos"

# ISODID
PENTAHO_ISODID_MEDIA_PATH = f"{PENTAHO_MEDIA_PATH}isodid/"
PENTAHO_ISODID_REPORT_NAME = "Indice_valutazione_Corso_di_Studi_tabella"
PENTAHO_ISODID_REPORT_PATH = f":public:spcanalisidati:Report per portale:{PENTAHO_ISODID_REPORT_NAME}.prpt"
PENTAHO_ISODID_REPORT_OUTPUT = "table/csv;page-mode=stream"
PENTAHO_ISODID_REPORT_PARAMS = "&PAR_QUEST=ISODID_STUD_{}&PAR_AA={}&PAR_CDS={}"

PENTAHO_ISODID_REPORT_START_YEAR = ""
