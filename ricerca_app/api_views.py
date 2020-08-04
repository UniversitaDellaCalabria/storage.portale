from django.shortcuts import render
from rest_framework import generics, viewsets, permissions

from . models import *
from . serializers import *


# permissions.IsAuthenticatedOrReadOnly
# allow authenticated users to perform any request. Requests for
# unauthorised users will only be permitted if the request method is
# one of the "safe" methods; GET, HEAD or OPTIONS

class ApiResourceList(generics.ListCreateAPIView):
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(user_ins=self.request.user)


class ApiResourceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user_mod=self.request.user)

# =================================================

class ApiDocenteList(ApiResourceList):
    description = 'Available Professors and Researchers'
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer


class ApiDocenteDetail(ApiResourceDetail):
    description = 'Detail of a Professor or Researcher'
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

# =================================================

class ApiRicercaAster1List(ApiResourceList):
    description = 'Available Aster 1'
    queryset = RicercaAster1.objects.all()
    serializer_class = RicercaAster1Serializer


class ApiRicercaAster1Detail(ApiResourceDetail):
    description = 'Aster 1 Details'
    queryset = RicercaAster1.objects.all()
    serializer_class = RicercaAster1Serializer

# =================================================

class ApiRicercaAster2List(ApiResourceList):
    description = 'Available Aster 2'
    queryset = RicercaAster2.objects.all()
    serializer_class = RicercaAster2Serializer


class ApiRicercaAster2Detail(ApiResourceDetail):
    description = 'Aster 2 Details'
    queryset = RicercaAster2.objects.all()
    serializer_class = RicercaAster2Serializer

# =================================================

class ApiRicercaErc1List(ApiResourceList):
    description = 'Available Erc 1'
    queryset = RicercaErc1.objects.all()
    serializer_class = RicercaErc1Serializer


class ApiRicercaErc1Detail(ApiResourceDetail):
    description = 'Erc 1 Details'
    queryset = RicercaErc1.objects.all()
    serializer_class = RicercaErc1Serializer

# =================================================

class ApiRicercaErc2List(ApiResourceList):
    description = 'Available Erc 2'
    queryset = RicercaErc2.objects.all()
    serializer_class = RicercaErc2Serializer


class ApiRicercaErc2Detail(ApiResourceDetail):
    description = 'Erc 2 Details'
    queryset = RicercaErc2.objects.all()
    serializer_class = RicercaErc2Serializer

# =================================================

class ApiRicercaDocenteGruppoList(ApiResourceList):
    description = 'List of Professors/Researchers in which Research Groups'
    queryset = RicercaDocenteGruppo.objects.all()
    serializer_class = RicercaDocenteGruppoSerializer

class ApiRicercaDocenteGruppoDetail(ApiResourceDetail):
    description = 'Details of Professors/Researchers in which Research Groups'
    queryset = RicercaDocenteGruppo.objects.all()
    serializer_class = RicercaDocenteGruppoSerializer


# =================================================

class ApiRicercaDocenteLineaApplicataList(ApiResourceList):
    description = 'List of Professors/Researchers and Applied Lines'
    queryset = RicercaDocenteLineaApplicata.objects.all()
    serializer_class = RicercaDocenteLineaApplicataSerializer

class ApiRicercaDocenteLineaApplicataDetail(ApiResourceDetail):
    description = 'Details of a Professor/Researcher in an Applied Line'
    queryset = RicercaDocenteLineaApplicata.objects.all()
    serializer_class = RicercaDocenteLineaApplicataSerializer

# =================================================

class ApiRicercaDocenteLineaBaseList(ApiResourceList):
    description = 'List of Base Lines'
    queryset = RicercaDocenteLineaBase.objects.all()
    serializer_class = RicercaDocenteLineaBaseSerializer

class ApiRicercaDocenteLineaBaseDetail(ApiResourceDetail):
    description = 'Details about a Base Line'
    queryset = RicercaDocenteLineaBase.objects.all()
    serializer_class = RicercaDocenteLineaBaseSerializer


# =================================================

class ApiRicercaGruppoList(ApiResourceList):
    description = 'List of Research Groups'
    queryset = RicercaGruppo.objects.all()
    serializer_class = RicercaGruppoSerializer

class ApiRicercaGruppoDetail(ApiResourceDetail):
    description = 'Details of a Research Group'
    queryset = RicercaGruppo.objects.all()
    serializer_class = RicercaGruppoSerializer

# =================================================

class ApiRicercaLineaApplicataList(ApiResourceList):
    description = 'List of Applied Lines'
    queryset = RicercaLineaApplicata.objects.all()
    serializer_class = RicercaLineaApplicataSerializer

class ApiRicercaLineaApplicataDetail(ApiResourceDetail):
    description = 'Detail of an Applied Line'
    queryset = RicercaLineaApplicata.objects.all()
    serializer_class = RicercaLineaApplicataSerializer

# =================================================

class ApiRicercaLineaBaseList(ApiResourceList):
    description = 'List of Base Lines'
    queryset = RicercaLineaBase.objects.all()
    serializer_class = RicercaLineaBaseSerializer

class ApiRicercaLineaBaseDetail(ApiResourceDetail):
    description = 'Details of a Base Line'
    queryset = RicercaLineaBase.objects.all()
    serializer_class = RicercaLineaBaseSerializer
