from django.urls import path

from .views import (
    ApiAster1List,
    ApiAster2List,
    ApiErc0List,
    ApiErc1List,
    ApiErc2List,
    ApiInfrastructuresList,
    ApiLaboratoriesAreasList,
    ApiLaboratoriesList,
    ApiLaboratoriesScopesList,
    ApiLaboratoryDetail,
)

app_name = "apiv1"

urlpatterns = [
    path("laboratories/<str:laboratoryid>/", ApiLaboratoryDetail.as_view(), name="laboratory-detail"),
    path("laboratories/", ApiLaboratoriesList.as_view(), name="laboratories-list"),
    path("laboratoriesareas/", ApiLaboratoriesAreasList.as_view(), name="laboratories-areas"),
    path("laboratories-scopes/", ApiLaboratoriesScopesList.as_view(), name="laboratories-scopes"),
    path('erc0list/', ApiErc0List.as_view(), name='erc0-list'),
    path('erc1list/', ApiErc1List.as_view(), name='erc1-list'),
    path('erc2list/', ApiErc2List.as_view(), name='erc2-list'),
    path('aster1list/', ApiAster1List.as_view(), name='aster1-list'),
    path('aster2list/', ApiAster2List.as_view(), name='aster2-list'),
    path('infrastructures/', ApiInfrastructuresList.as_view(), name='infrastructures'),
]