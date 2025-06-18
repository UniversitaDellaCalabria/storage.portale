from rest_framework.routers import DefaultRouter
from .views import (
    TeachersViewSet,
    CoveragesViewSet,
    PublicationsViewSet,
    TeachersStudyActivitiesViewSet,
    TeachersMaterialsViewSet,
    TeachersBaseResearchLinesViewSet,
    TeachersNewsViewSet,
    PublicationsCommunityTypesViewSet,
    TeachersAppliedResearchLinesViewSet
    # TeachersCoverageStudyActivitiesViewSet,
    # TeachersCoveragePublicationsViewSet,
    # TeachersPublicationsViewSet,
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"teachers", TeachersViewSet, basename="teachers")
router.register(
    r"teachers/studyactivities",
    TeachersStudyActivitiesViewSet,
    basename="teachers-studyactivities",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/materials",
    TeachersMaterialsViewSet,
    basename="teachers-materials",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/researchlines/base",
    TeachersBaseResearchLinesViewSet,
    basename="teachers-researchlines-base",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/researchlines/applicata",
    TeachersAppliedResearchLinesViewSet,
    basename="teachers-researchlines-applicata",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/news",
    TeachersNewsViewSet,
    basename="teachers-news",
)
router.register(r"publications", PublicationsViewSet, basename="publications")
router.register(
    r"publicationscommunitytypes",
    PublicationsCommunityTypesViewSet,
    basename="publicationscommunitytypes",
)
router.register(r"coverages", CoveragesViewSet, basename="coverages")
urlpatterns += router.urls
