from django.conf import settings
from django.utils.translation import gettext_lazy as _

# regdid status change email config
STATUS_EMAIL_SUBJECT = getattr(settings, "STATUS_EMAIL_SUBJECT", _("Didactic Regulation App"))
STATUS_EMAIL_MESSAGE_DEPARTMENT = getattr(settings, "STATUS_EMAIL_MESSAGE_DEPARTMENT" ,_("Requested changes for the didactic regulation"))
STATUS_EMAIL_MESSAGE_REVISION = getattr(settings, "STATUS_EMAIL_MESSAGE_REVISION" ,_("Requested revision for the didactic regulation"))
STATUS_EMAIL_MESSAGE_APPROVAL = getattr(settings, "STATUS_EMAIL_MESSAGE_APPROVAL" ,_("Requested approval for the didactic regulation"))
STATUS_EMAIL_FROM = getattr(settings, "STATUS_EMAIL_FROM", "noreply@unical.it")