from django.urls import path

from .views import (
    ApiAddressbookFullList,
    ApiAddressbookList,
    ApiAddressbookStructuresList,
    ApiDecryptedPersonId,
    ApiPersonaleDetail,
    ApiPersonaleFullDetail,
    ApiPersonId,
    ApiPersonnelCfList,
    ApiRolesList,
)

from structures.api.v1.views import ApiStructureDetail

app_name = "apiv1"

urlpatterns = [
    path("get-person-id/", ApiPersonId.as_view(), name="get-person-id"),
    path("get-decrypted-person-id/", ApiDecryptedPersonId.as_view(), name="get-decrypted-person-id"),
    path("personnel-cfs/", ApiPersonnelCfList.as_view(), name="personnel-cfs"),
    path("addressbook/", ApiAddressbookList.as_view(), name="addressbook-list"),
    path("addressbook-full/", ApiAddressbookFullList.as_view(), name="addressbook-list-full"),
    path("addressbook/<str:personaleid>/", ApiPersonaleDetail.as_view(), name="personale-detail"),
    path("addressbook-full/<str:personaleid>/", ApiPersonaleFullDetail.as_view(), name="personale-detail-full"),
    path("addressbookstructures/", ApiAddressbookStructuresList.as_view(), name="all-structures-list"),
    path("addressbookstructures/<str:structureid>/", ApiStructureDetail.as_view(), name="addressbook-structure-detail"),  # TODO duplicate
    path("roles/", ApiRolesList.as_view(), name="roles-list"),
]
