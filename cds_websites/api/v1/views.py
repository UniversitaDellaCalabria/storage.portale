import json

import requests
from django.conf import settings
from django.db.models import Q
from generics.views import ApiEndpointList
from organizational_area.models import OrganizationalStructureOfficeEmployee
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from cds_websites.models import SitoWebCdsOggettiPortale
from cds_websites.settings import OFFICE_CDS_WEBSITES

from .filters import (
    CdsWebsitesTopicArticlesListFilter,
    CdsWebsitesStudyPlansListFilter,
)
from .serializers import (
    CdsWebsitesTopicArticlesSerializer,
    CdsWebsitesTopicSerializer,
    SitoWebCdsOggettiPortaleSerializer,
    CdsWebsitesStudyPlansSerializer,
)
from .services import ServiceSitoWebCds


class SitoWebCdsOggettiPortaleViewSet(ReadOnlyModelViewSet):
    description = "Retrieves a list of objects for the management crud."
    serializer_class = SitoWebCdsOggettiPortaleSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    schema = None
    pagination_class = None

    def get_queryset(self):
        if self.action != "list":
            return SitoWebCdsOggettiPortale.objects.all()

        cds_id = self.kwargs.get("cds_id")

        search_query = self.request.query_params.get("search", "")

        if not search_query:
            return SitoWebCdsOggettiPortale.objects.none()

        queryset = SitoWebCdsOggettiPortale.objects.filter(cds_id=cds_id).filter(
            Q(titolo_it__icontains=search_query) | Q(titolo_en__icontains=search_query)
        )
        return queryset


class ExternalOggettiPortaleViewSet(GenericViewSet):
    description = "Retrieves a list of external objects for the management crud."
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    schema = None
    pagination_class = None

    def list(self, request):
        UNICMS_AUTH_TOKEN = getattr(settings, "UNICMS_AUTH_TOKEN", "")
        UNICMS_ROOT_URL = getattr(settings, "UNICMS_ROOT_URL", "")
        UNICMS_OBJECT_API = getattr(settings, "UNICMS_OBJECT_API", {})

        object_class = request.query_params.get("object_class", None)
        search = request.query_params.get("search", None)

        if (
            object_class is None
            or object_class not in UNICMS_OBJECT_API.keys()
            or object_class == "WebPath"
        ):
            return Response(
                {"error": "Bad object class"}, status=status.HTTP_400_BAD_REQUEST
            )

        url = UNICMS_OBJECT_API[object_class]
        headers = {"Authorization": f"Token {UNICMS_AUTH_TOKEN}"}
        params = {"search": search, "format": "json"}
        try:
            response_obj = {}
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()

            json_response = json.loads(response._content)
            response_obj["count"] = json_response.get("count", None)
            response_obj["results"] = []
            response_obj["object_class"] = object_class
            for result in json_response.get("results", []):
                result_obj = {}
                if object_class == "Publication":
                    result_obj["object_class"] = object_class
                    result_obj["id"] = result.get("id", None)
                    result_obj["title"] = result.get("title", None)
                    result_obj["subheading"] = result.get("subheading", None)
                else:
                    result_obj["object_class"] = object_class
                    result_obj["id"] = result.get("id", None)
                    result_obj["name"] = result.get("name", None)
                    result_obj["content"] = UNICMS_ROOT_URL + result.get(
                        "get_full_path", None
                    )
                response_obj["results"].append(result_obj)

            return Response(response_obj)
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code"):
                return Response({"error": str(e)}, status=e.response.status_code)
            else:
                return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    def retrieve(self, request, pk=None):
        UNICMS_AUTH_TOKEN = getattr(settings, "UNICMS_AUTH_TOKEN", "")
        UNICMS_OBJECT_API = getattr(settings, "UNICMS_OBJECT_API", {})

        object_class = request.query_params.get("object_class", None)

        if object_class is None or object_class not in UNICMS_OBJECT_API.keys():
            return Response(
                {"error": "Bad object class"}, status=status.HTTP_400_BAD_REQUEST
            )

        url = f"{UNICMS_OBJECT_API[object_class]}{pk}/"
        headers = {"Authorization": f"Token {UNICMS_AUTH_TOKEN}"}
        params = {"format": "json"}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            response_json = response.json()
            response_json["object_class"] = object_class
            return Response(response_json)
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code"):
                return Response({"error": str(e)}, status=e.response.status_code)
            else:
                return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class ApiCdsWebsitesTopicList(ApiEndpointList):
    description = "Retrieves the list of topics of the cds web sites."
    serializer_class = CdsWebsitesTopicSerializer

    def get_queryset(self):
        return ServiceSitoWebCds.getCdsWebsitesTopics()


class ApiCdsWebsitesTopicArticlesList(ApiEndpointList):
    description = "Retrieves the list of items (regulament articles, sub articles, objects, extras) of cds web sites."
    serializer_class = CdsWebsitesTopicArticlesSerializer
    filter_backends = [CdsWebsitesTopicArticlesListFilter]

    def get_queryset(self):
        request = self.request
        cds_cod = self.request.query_params.get("cds_cod")
        topic_id = self.request.query_params.get("topic_id")

        # get only active elements if public
        # get all elements if in CRUD backend
        only_active = True
        if request.user.is_superuser:
            only_active = False  # pragma: no cover
        elif request.user.is_authenticated:  # pragma: no cover
            offices = OrganizationalStructureOfficeEmployee.objects.filter(
                employee=request.user,
                office__is_active=True,
                office__name=OFFICE_CDS_WEBSITES,
                office__organizational_structure__is_active=True,
            )

            if offices.exists():
                only_active = False

        return ServiceSitoWebCds.getCdsWebsitesTopicArticles(
            cds_cod, topic_id, only_active
        )


class ApiCdsWebsitesStudyPlansList(ApiEndpointList):
    description = "Retrieves the list of study plans for courses of study."
    serializer_class = CdsWebsitesStudyPlansSerializer
    filter_backends = [CdsWebsitesStudyPlansListFilter]

    def get_queryset(self):
        cds_cod = self.request.query_params.get("cds_cod")
        year = self.request.query_params.get("year")
        return ServiceSitoWebCds.getCdsWebsitesStudyPlans(cds_cod, year)

    def get(self, *args, **kwargs):
        lang = self.request.LANGUAGE_CODE
        self.language = self.request.query_params.get("lang", lang).lower()
        cds_cod = self.request.query_params.get("cds_cod")
        year = self.request.query_params.get("year")
        cache_key = f"cdswebsite_studyplanlist_{self.language}__{cds_cod}_{year}"
        kwargs["cache_key"] = cache_key
        return super().get(*args, **kwargs)
