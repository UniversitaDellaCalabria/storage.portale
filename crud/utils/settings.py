from django.conf import settings
from django.utils.translation import gettext_lazy as _


OFFICE_RESEARCHGROUPS = getattr(settings, 'OFFICE_RESEARCHGROUPS', 'researchgroups')
OFFICE_RESEARCHLINES = getattr(settings, 'OFFICE_RESEARCHLINES', 'researchlines')
OFFICE_CDS = getattr(settings, 'OFFICE_CDS', 'cds')
OFFICE_PATENTS = getattr(settings, 'OFFICE_PATENTS', 'patents')
OFFICE_COMPANIES = getattr(settings, 'OFFICE_COMPANIES', 'companies')
OFFICE_PROJECTS = getattr(settings, 'OFFICE_PROJECTS', 'projects')
OFFICE_TEACHERS = getattr(settings, 'OFFICE_TEACHERS', 'teachers')
OFFICE_PHD = getattr(settings, 'OFFICE_PHD', 'phd')


ALLOWED_CDS_LANGUAGES = ['ita', 'eng']
ALLOWED_CDS_JOINT_DEGREES = [
    {'COD': 'N', 'name': _("No")},
    {'COD': 'S', 'name': _("Joint title")},
    {'COD': 'D', 'name': _("Double title")}
]
CMS_STORAGE_ROOT_API = 'https://pp.storage.unical.it'
