from django.utils.translation import gettext_lazy as _


OFFICE_RESEARCHGROUPS = 'researchgroups'
OFFICE_RESEARCHLINES = 'researchlines'
OFFICE_CDS = 'cds'

ALLOWED_CDS_LANGUAGES = ['ita', 'eng']
ALLOWED_CDS_JOINT_DEGREES = [
    {'COD': 'N', 'name': _("No")},
    {'COD': 'S', 'name': _("Joint title")},
    {'COD': 'D', 'name': _("Double title")}
]
CURRENT_YEAR = ""


