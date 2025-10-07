from generics.utils import decrypt, encrypt
from generics.views import ApiEndpointDetail, ApiEndpointList, ApiEndpointListSupport
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi_agid import AgidAutoSchema
from rest_framework.views import APIView
from teachers.api.v1.services import ServiceDocente

from addressbook.models import Personale
from addressbook.utils import get_personale_matricola

from .filters import (
    AddressbookListFilter,
    AddressbookStructuresListFilter,
    PersonnelCfListFilter,
)
from .schemas import ApiDecryptedPersonIdSchema, ApiPersonIdSchema
from .serializers import (
    AddressbookFullSerializer,
    AddressbookSerializer,
    AddressbookStructuresSerializer,
    PersonaleFullSerializer,
    PersonaleSerializer,
    PersonnelCfSerializer,
    RolesSerializer,
)
from .services import ServicePersonale


class ApiAddressbookList(ApiEndpointList):
    description = "Retrieves the personnel address book."
    serializer_class = AddressbookSerializer
    filter_backends = [AddressbookListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        phone = request.query_params.get("phone")
        structureid = request.query_params.get("structure")
        structuretypes = request.query_params.get("structuretypes")
        role = request.query_params.get("role")
        structuretree = request.query_params.get("structuretree")

        return ServicePersonale.getAddressbook(
            search, structureid, structuretypes, role, structuretree, phone
        )


class ApiAddressbookFullList(ApiEndpointList):
    description = "Retrieves the personnel address book with additional contract data."
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressbookFullSerializer
    filter_backends = [AddressbookListFilter]
    schema = AgidAutoSchema(tags=["api"])

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        phone = request.query_params.get("phone")
        structureid = request.query_params.get("structure")
        structuretypes = request.query_params.get("structuretypes")
        role = request.query_params.get("role")
        structuretree = request.query_params.get("structuretree")
        taxpayer_id = request.query_params.get("taxpayer_id")

        return ServicePersonale.getAddressbook(
            search=search,
            structureid=structureid,
            structuretypes=structuretypes,
            role=role,
            structuretree=structuretree,
            phone=phone,
            taxpayer_id=taxpayer_id,
            full=True,
        )


class ApiRolesList(ApiEndpointListSupport):
    description = "Retrieves a list of roles of the personnel."
    serializer_class = RolesSerializer

    def get_queryset(self):
        return ServiceDocente.getRoles()


class ApiPersonaleDetail(ApiEndpointDetail):
    description = "Retrieves detailed information of a specific person."
    serializer_class = PersonaleSerializer

    def get_queryset(self):
        personaleid = self.kwargs["personaleid"]
        return ServicePersonale.getPersonale(personale_id=personaleid)


class ApiPersonaleFullDetail(ApiEndpointDetail):
    description = (
        "Retrieves detailed information of a specific person, including contract data."
    )
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaleFullSerializer
    schema = AgidAutoSchema(tags=["api"])

    def get_queryset(self):
        personaleid = self.kwargs["personaleid"]
        return ServicePersonale.getPersonale(personale_id=personaleid, full=True)


class ApiAddressbookStructuresList(ApiEndpointList):
    description = "Retrieves the organizational structures a person is affiliated with."
    serializer_class = AddressbookStructuresSerializer
    filter_backends = [AddressbookStructuresListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        father = request.query_params.get("father")
        type = request.query_params.get("type")

        return ServicePersonale.getAllStructuresList(search, father, type)


class ApiPersonnelCfList(ApiEndpointList):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "Retrieves the list of personnel tax codes."
    serializer_class = PersonnelCfSerializer
    filter_backends = [PersonnelCfListFilter]
    schema = AgidAutoSchema(tags=["api"])

    def get_queryset(self):
        roles = self.request.query_params.get("roles")
        return ServicePersonale.getPersonnelCfs(roles)


class ApiPersonId(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "Retrieves the encrypted matricola of a person."
    schema = ApiPersonIdSchema()

    def post(self, request, *args, **kwargs):
        data = request.data
        matricola = data.get("id", "")
        if not matricola:
            return Response(
                "Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND
            )
        p = Personale.objects.filter(matricola=matricola).first()
        if not p:
            return Response("Il dato non esiste", status=status.HTTP_404_NOT_FOUND)
        return Response(encrypt(matricola))


class ApiDecryptedPersonId(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "Retrieves the decypted matricola of a person."
    schema = ApiDecryptedPersonIdSchema()

    def post(self, request, *args, **kwargs):
        data = request.data
        encrypted_matricola = data.get("id", "")
        if not encrypted_matricola:
            return Response(
                "Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND
            )
        return Response(get_personale_matricola(encrypted_matricola))
        # ~ try:
            # ~ m = decrypt(encrypted_matricola)
            # ~ return Response(m)
        # ~ except Exception:
            # ~ return Response(
                # ~ "Non è stato possibile decriptare il dato",
                # ~ status=status.HTTP_404_NOT_FOUND,
            # ~ )
