from addressbook.models import Personale
from generics.utils import decrypt, encrypt
from generics.views import ApiEndpointDetail, ApiEndpointList, ApiEndpointListSupport
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from structures.api.v1.filters import ApiStructuresListFilter
from structures.api.v1.views import ApiStructureDetail
from teachers.api.v1.services import ServiceDocente

from .filters import ApiAddressbookListFilter
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
    description = "La funzione restituisce la rubrica telefonica del personale"
    serializer_class = AddressbookSerializer
    filter_backends = [ApiAddressbookListFilter]

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
    description = "La funzione restituisce la rubrica telefonica del personale arricchita con dati riguardanti il contratto"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressbookFullSerializer
    filter_backends = [ApiAddressbookListFilter]

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
    description = "La funzione restituisce i ruoli"
    serializer_class = RolesSerializer
    filter_backends = []

    def get_queryset(self):
        return ServiceDocente.getRoles()


class ApiPersonaleDetail(ApiEndpointDetail):
    description = "La funzione restituisce una specifica persona"
    serializer_class = PersonaleSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        personaleid = self.kwargs["personaleid"]
        return ServicePersonale.getPersonale(personale_id=personaleid)


class ApiPersonaleFullDetail(ApiEndpointDetail):
    description = (
        "La funzione restituisce una specifica persona con i dati sul contratto"
    )
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PersonaleFullSerializer
    # filter_backends = [ApiAddressbookListFilter]

    def get_queryset(self):
        personaleid = self.kwargs["personaleid"]
        return ServicePersonale.getPersonale(personale_id=personaleid, full=True)


class ApiAddressbookStructuresList(ApiEndpointList):
    description = (
        "La funzione restituisce le strutture organizzative a cui un docente afferisce"
    )
    serializer_class = AddressbookStructuresSerializer
    filter_backends = [ApiStructuresListFilter]

    def get_queryset(self):
        request = self.request
        search = request.query_params.get("search")
        father = request.query_params.get("father")
        type = request.query_params.get("type")

        return ServicePersonale.getAllStructuresList(search, father, type)


class AddressbookStructureDetail(AutoSchema):
    def get_operation(self, path, method):  
        operation = super().get_operation(path, method)
        operation['operationId'] = "retrieveAddressbookStructureDetail" 
        return operation
        


class ApiAddressbookStructureDetail(ApiStructureDetail):
    schema = AddressbookStructureDetail()


class ApiPersonnelCfList(ApiEndpointList):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "La funzione restituisce la lista dei cf del personale"
    serializer_class = PersonnelCfSerializer
    filter_backends = []

    def get_queryset(self):
        roles = self.request.query_params.get("roles")
        return ServicePersonale.getPersonnelCfs(roles)


class ApiPersonIdSchema(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "getPersonId" 
        return operation



class ApiPersonId(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "La funzione restituisce il codice criptato di una persona"
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


class ApiDecryptedPersonIdSchema(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation['operationId'] = "getDecryptedPersonId" 
        return operation


class ApiDecryptedPersonId(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    description = "La funzione restituisce la matricola in chiaro una persona"
    schema = ApiDecryptedPersonIdSchema()

    def post(self, request, *args, **kwargs):
        data = request.data
        encrypted_matricola = data.get("id", "")
        if not encrypted_matricola:
            return Response(
                "Il dato non è stato inserito", status=status.HTTP_404_NOT_FOUND
            )
        try:
            m = decrypt(encrypted_matricola)
            return Response(m)
        except Exception:
            return Response(
                "Non è stato possibile decriptare il dato",
                status=status.HTTP_404_NOT_FOUND,
            )
