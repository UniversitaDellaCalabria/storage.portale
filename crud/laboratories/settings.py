from django.conf import settings
from django.utils.translation import gettext_lazy as _

#EMAIL PARAMETERS TO VALIDATORS
TO_VALIDATORS_EMAIL_SUBJECT = getattr(settings, "TO_VALIDATORS_EMAIL_SUBJECT", _("Request for Laboratory Validation"))
TO_VALIDATORS_EMAIL_MESSAGE = getattr(settings, "TO_VALIDATORS_EMAIL_MESSAGE" ,_("Needed validaton for laboratory"))
TO_VALIDATORS_EMAIL_FROM = getattr(settings, "TO_VALIDATORS_EMAIL_FROM", "noreply@unical.it")