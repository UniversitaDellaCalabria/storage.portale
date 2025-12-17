# advanced_training/settings.py
from django.conf import settings

HIGH_FORMATION_YEAR = getattr(settings, 'HIGH_FORMATION_YEAR', '')

OFFICE_ADVANCED_TRAINING_VALIDATOR = getattr(settings, 'OFFICE_ADVANCED_TRAINING_VALIDATOR', 'master_validators')
OFFICE_ADVANCED_TRAINING = getattr(settings, 'OFFICE_ADVANCED_TRAINING', 'master')