from django.urls import path
from . views import ApiCdsWebsiteTimetable, ApiCdsWebsiteExams

app_name = "apiv1"

urlpatterns = [
    path('cds-websites/<str:cdswebsitecod>/timetable/', ApiCdsWebsiteTimetable.as_view(), name='cdswebsite-timetable'),
    path('cds-websites/<str:cdswebsitecod>/exams/', ApiCdsWebsiteExams.as_view(), name='cdswebsite-exams'),
]
