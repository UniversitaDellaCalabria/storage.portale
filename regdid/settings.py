from django.conf import settings
from django.utils.translation import gettext_lazy as _

OFFICE_REGDIDS_DEPARTMENT = getattr(settings, 'OFFICE_REGDIDS_DEPARTMENT', 'regdids_department')
OFFICE_REGDIDS_REVISION = getattr(settings, 'OFFICE_REGDIDS_REVISION', 'regdids_revision')
OFFICE_REGDIDS_APPROVAL = getattr(settings, 'OFFICE_REGDIDS_APPROVAL', 'regdids_approval')

# regdid status change email config
STATUS_EMAIL_SUBJECT = getattr(settings, "STATUS_EMAIL_SUBJECT", _("Didactic Regulation App"))
STATUS_EMAIL_MESSAGE_DEPARTMENT = getattr(settings, "STATUS_EMAIL_MESSAGE_DEPARTMENT", _("Requested changes for the didactic regulation"))
STATUS_EMAIL_MESSAGE_REVISION = getattr(settings, "STATUS_EMAIL_MESSAGE_REVISION", _("Requested revision for the didactic regulation"))
STATUS_EMAIL_MESSAGE_APPROVAL = getattr(settings, "STATUS_EMAIL_MESSAGE_APPROVAL", _("Requested approval for the didactic regulation"))
STATUS_EMAIL_FROM = getattr(settings, "STATUS_EMAIL_FROM", "noreply@unical.it")

REGDID_ALLOWED_COURSE_TYPES = getattr(settings, 'REGDID_ALLOWED_COURSE_TYPES', ['L', 'LM', 'LM5', 'LM6'])

REGDID_CKEDITOR_FORCE_PASTE_AS_PLAIN_TEXT = getattr(settings, 'REGDID_CKEDITOR_FORCE_PASTE_AS_PLAIN_TEXT', False)
