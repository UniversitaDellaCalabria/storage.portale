# advanced_training/settings.py
from django.conf import settings

ADVANCED_TRAINING_YEAR = getattr(settings, 'ADVANCED_TRAINING_YEAR', '')

OFFICE_ADVANCED_TRAINING_VALIDATOR = getattr(settings, 'OFFICE_ADVANCED_TRAINING_VALIDATOR', 'master_validators')
OFFICE_ADVANCED_TRAINING = getattr(settings, 'OFFICE_ADVANCED_TRAINING', 'master')

ADVANCED_TRAINING_MEDIA_PATH_BASE = getattr(settings, "ADVANCED_TRAINING_MEDIA_PATH_BASE", "portale/alta_formazione/")
def advanced_training_media_path(instance, filename):
    return f'{ADVANCED_TRAINING_MEDIA_PATH_BASE}{filename}'

