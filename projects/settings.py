from django.conf import settings

OFFICE_PROJECTS = getattr(settings, 'OFFICE_PROJECTS', 'projects')
