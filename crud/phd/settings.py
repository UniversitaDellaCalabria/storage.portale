from django.conf import settings


PHD_CYCLES = [(38, 'XXXVIII'), (39, 'XXXIX')]

STRUCTURE_PHD = getattr(
    settings, 'STRUCTURE_PHD', 'phd-management')

PHD_DEFAULT_OFFICE = getattr(
    settings, 'PHD_DEFAULT_OFFICE', 'default')
