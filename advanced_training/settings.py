from django.conf import settings

HIGH_FORMATION_YEAR = getattr(settings, 'HIGH_FORMATION_YEAR', '')

OFFICE_ADVANCED_TRAINING = getattr(settings, 'OFFICE_ADVANCED_TRAINING', 'advanced_training')
OFFICE_ADVANCED_TRAINING_VALIDATORS = getattr(settings, 'OFFICE_ADVANCED_TRAINING_VALIDATORS', 'advanced_training_validators')