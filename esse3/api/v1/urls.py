from django.urls import path
from . views import ApiCdsWebsiteTimetable, ApiCdsWebsiteExams

app_name = "apiv1"

urlpatterns = [
    path('cds-websites/<str:cds_cod>/timetable/', ApiCdsWebsiteTimetable.as_view(), name='cdswebsite-timetable'),
    path('cds-websites/<str:cds_cod>/exams/', ApiCdsWebsiteExams.as_view(), name='cdswebsite-exams'),
]
