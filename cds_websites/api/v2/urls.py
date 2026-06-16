from rest_framework.routers import DefaultRouter
from .views import TopicListViewSet, ArticlesTopicListViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"topic-list", TopicListViewSet, basename="topic-list")
router.register(
    r"topic-articles/(?P<cds_cod>\d+)/(?P<topic_id>\d+)",
    ArticlesTopicListViewSet,
    basename="topic-articles",
)

urlpatterns += router.urls
