from django.conf import settings

HIGH_FORMATION_YEAR = getattr(settings, 'HIGH_FORMATION_YEAR', '')

OFFICE_ADVANCED_TRAINING_SENDER = getattr(settings, 'OFFICE_ADVANCED_TRAINING_SENDER', 'master_senders')
OFFICE_ADVANCED_TRAINING_VALIDATOR = getattr(settings, 'OFFICE_ADVANCED_TRAINING_VALIDATOR', 'master_validators')