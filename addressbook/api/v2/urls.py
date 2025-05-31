from rest_framework.routers import DefaultRouter
from .views import (
    GetPersonApi,
    GetDecryptedPersonApi,
    PersonnelCfViewSet,
    AddressbookViewSet,
)  # , RolesViewSet, AddressbookStructuresViewSet

app_name = "apiv2"

router = DefaultRouter()

urlpatterns = []

router.register(r"get-person-id", GetPersonApi, basename="get-person-id")
router.register(
    r"get-decrypted-person-id",
    GetDecryptedPersonApi,
    basename="get-decrypted-person-id",
)
router.register(r"personnel-cfs", PersonnelCfViewSet, basename="personnel-cfs")
router.register(r"addressbook", AddressbookViewSet, basename="addressbook")
# router.register(r"addressbook-full", AddressbookFullViewSet, basename="addressbook-full")
# router.register(r"addressbookstructures", AddressbookStructuresViewSet, basename="addressbookstructures")
# router.register(r"roles", RolesViewSet, basename="roles")

urlpatterns += router.urls
