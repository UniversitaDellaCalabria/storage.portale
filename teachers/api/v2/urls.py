from rest_framework.routers import DefaultRouter
from .views import (
    TeachersViewSet,
    CoveragesViewSet,
    PublicationsViewSet,
    TeachersStudyActivitiesViewSet,
    TeachersMaterialsViewSet,
    TeachersResearchLinesViewSet,
    TeachersNewsViewSet,
    PublicationsCommunityTypesViewSet,
    # TeachersCoverageStudyActivitiesViewSet,
    # TeachersCoveragePublicationsViewSet,
    # TeachersPublicationsViewSet,
)

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"teachers", TeachersViewSet, basename="teachers")
router.register(
    r"teachers/(?P<id>[^/.]+)/studyactivities",
    TeachersStudyActivitiesViewSet,
    basename="teachers-studyactivities",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/materials",
    TeachersMaterialsViewSet,
    basename="teachers-materials",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/researchlines",
    TeachersResearchLinesViewSet,
    basename="teachers-researchlines",
)
router.register(
    r"teachers/(?P<id>[^/.]+)/news",
    TeachersNewsViewSet,
    basename="teachers-news",
)
router.register(
    r"publicationscommunitytypes",
    PublicationsCommunityTypesViewSet,
    basename="publicationscommunitytypes",
)
router.register(r"coverages", CoveragesViewSet, basename="coverages")
router.register(r"publications", PublicationsViewSet, basename="publications")

# router.register(
#     r"teachers/(?P<id>[^/.]+)/publications",
#     TeachersPublicationsViewSet,
#     basename="teachers-publications",
# )
# router.register(
#     r"coverages/(?P<id>[^/.]+)/studyactivities",
#     TeachersCoverageStudyActivitiesViewSet,
#     basename="teachers-coverages-studyactivities",
# )
# router.register(
#     r"coverages/(?P<id>[^/.]+)/publications",
#     TeachersCoveragePublicationsViewSet,
#     basename="teachers-coverages-publications",
# )

urlpatterns += router.urls
