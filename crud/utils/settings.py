from django.conf import settings
from django.utils.translation import gettext_lazy as _


STRUCTURE_PHD = getattr(
    settings, 'STRUCTURE_PHD', 'phd-management')

OFFICE_RESEARCHGROUPS = getattr(
    settings, 'OFFICE_RESEARCHGROUPS', 'researchgroups')
OFFICE_RESEARCHLINES = getattr(
    settings, 'OFFICE_RESEARCHLINES', 'researchlines')
OFFICE_CDS = getattr(settings, 'OFFICE_CDS', 'cds')
OFFICE_CDS_WEBSITES = getattr(settings, 'OFFICE_CDS_WEBSITES', 'cds_websites')
OFFICE_CDS_DOCUMENTS = getattr(settings, 'OFFICE_CDS_DOCUMENTS', 'cds_documents')
OFFICE_CDS_TEACHING_SYSTEM = getattr(settings, 'OFFICE_CDS_TEACHING_SYSTEM', 'cds_teaching_system')
OFFICE_PATENTS = getattr(settings, 'OFFICE_PATENTS', 'patents')
OFFICE_COMPANIES = getattr(settings, 'OFFICE_COMPANIES', 'companies')
OFFICE_PROJECTS = getattr(settings, 'OFFICE_PROJECTS', 'projects')
OFFICE_TEACHERS = getattr(settings, 'OFFICE_TEACHERS', 'teachers')
OFFICE_LABORATORIES = getattr(settings, 'OFFICE_LABORATORIES', 'laboratories')
OFFICE_LABORATORY_VALIDATORS = getattr(settings, 'OFFICE_LABORATORIES', 'laboratory_validators')

ALLOWED_CDS_LANGUAGES = ['ita', 'eng']
ALLOWED_CDS_JOINT_DEGREES = [
    {'COD': 'N', 'name': _("No")},
    {'COD': 'S', 'name': _("Joint title")},
    {'COD': 'D', 'name': _("Double title")}
]
CMS_STORAGE_ROOT_API = 'https://pp.storage.unical.it'
STRUCTURES_FATHER = ''
ALLOWED_STRUCTURE_TYPES = []

UNICMS_AUTH_TOKEN = getattr(settings, "UNICMS_AUTH_TOKEN", "")
UNICMS_TOPIC_API_URL = getattr(settings, "UNICMS_TOPIC_API_URL", "")
UNICMS_ROOT_URL = getattr(settings, "UNICMS_ROOT_URL", "")
UNICMS_PUBLICATION_API_URL = getattr(settings, "UNICMS_PUBLICATION_API_URL", "")
UNICMS_WEBPATH_API_URL = getattr(settings, "UNICMS_WEBPATH_API_URL", "")
UNICMS_OBJECT_API = getattr(settings, "UNICMS_OBJECT_API", {})

ETL_USER_IDS = getattr(settings, "ETL_USER_IDS", [])