from django.conf import settings


PHD_CYCLES = getattr(
    settings, 'PHD_CYCLES', []
)

STRUCTURE_PHD = getattr(
    settings, 'STRUCTURE_PHD', 'phd-management')

PHD_DEFAULT_OFFICE = getattr(
    settings, 'PHD_DEFAULT_OFFICE', 'default')

PHD_ADDITIONAL_REF_STRUCTURES = getattr(
    settings, 'PHD_ADDITIONAL_REF_STRUCTURES', [])
