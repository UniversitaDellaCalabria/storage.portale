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
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer


class ApiDocenteDetail(ApiResourceDetail):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

# =================================================

class ApiRicercaAster1List(ApiResourceList):
    queryset = RicercaAster1.objects.all()
    serializer_class = RicercaAster1Serializer


class ApiRicercaAster1Detail(ApiResourceDetail):
    queryset = RicercaAster1.objects.all()
    serializer_class = RicercaAster1Serializer

# =================================================

class ApiRicercaAster2List(ApiResourceList):
    queryset = RicercaAster2.objects.all()
    serializer_class = RicercaAster2Serializer


class ApiRicercaAster2Detail(ApiResourceDetail):
    queryset = RicercaAster2.objects.all()
    serializer_class = RicercaAster2Serializer

# =================================================

class ApiRicercaErc1List(ApiResourceList):
    queryset = RicercaErc1.objects.all()
    serializer_class = RicercaErc1Serializer


class ApiRicercaErc1Detail(ApiResourceDetail):
    queryset = RicercaErc1.objects.all()
    serializer_class = RicercaErc1Serializer

# =================================================

class ApiRicercaErc2List(ApiResourceList):
    queryset = RicercaErc2.objects.all()
    serializer_class = RicercaErc2Serializer


class ApiRicercaErc2Detail(ApiResourceDetail):
    queryset = RicercaErc2.objects.all()
    serializer_class = RicercaErc2Serializer

# =================================================

class ApiRicercaDocenteGruppoList(ApiResourceList):
    queryset = RicercaDocenteGruppo.objects.all()
    serializer_class = RicercaDocenteGruppoSerializer

class ApiRicercaDocenteGruppoDetail(ApiResourceDetail):
    queryset = RicercaDocenteGruppo.objects.all()
    serializer_class = RicercaDocenteGruppoSerializer


# =================================================

class ApiRicercaDocenteLineaApplicataList(ApiResourceList):
    queryset = RicercaDocenteLineaApplicata.objects.all()
    serializer_class = RicercaDocenteLineaApplicataSerializer

class ApiRicercaDocenteLineaApplicataDetail(ApiResourceDetail):
    queryset = RicercaDocenteLineaApplicata.objects.all()
    serializer_class = RicercaDocenteLineaApplicataSerializer

# =================================================

class ApiRicercaDocenteLineaBaseList(ApiResourceList):
    queryset = RicercaDocenteLineaBase.objects.all()
    serializer_class = RicercaDocenteLineaBaseSerializer

class ApiRicercaDocenteLineaBaseDetail(ApiResourceDetail):
    queryset = RicercaDocenteLineaBase.objects.all()
    serializer_class = RicercaDocenteLineaBaseSerializer


# =================================================

class ApiRicercaGruppoList(ApiResourceList):
    queryset = RicercaGruppo.objects.all()
    serializer_class = RicercaGruppoSerializer

class ApiRicercaGruppoDetail(ApiResourceDetail):
    queryset = RicercaGruppo.objects.all()
    serializer_class = RicercaGruppoSerializer

# =================================================

class ApiRicercaLineaApplicataList(ApiResourceList):
    queryset = RicercaLineaApplicata.objects.all()
    serializer_class = RicercaLineaApplicataSerializer

class ApiRicercaLineaApplicataDetail(ApiResourceDetail):
    queryset = RicercaLineaApplicata.objects.all()
    serializer_class = RicercaLineaApplicataSerializer

# =================================================

class ApiRicercaLineaBaseList(ApiResourceList):
    queryset = RicercaLineaBase.objects.all()
    serializer_class = RicercaLineaBaseSerializer

class ApiRicercaLineaBaseDetail(ApiResourceDetail):
    queryset = RicercaLineaBase.objects.all()
    serializer_class = RicercaLineaBaseSerializer
