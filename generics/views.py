from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.schemas.openapi_agid import AgidAutoSchema

from .pagination import UnicalStorageApiPaginationList
from .utils import encode_labels


@login_required
def home(request):
    return render(request, "dashboard.html")


class ApiEndpointList(generics.ListAPIView):
    pagination_class = UnicalStorageApiPaginationList
    permission_classes = [permissions.AllowAny]
    # filter_backends = [OrderingFilter]
    # ordering_fields = '__all__'
    allowed_methods = ("GET",)
    schema = AgidAutoSchema(tags = ['public'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = None

    def prepare_data(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return serializer

    def get(self, obj, **kwargs):
        if not self.language:
            lang = self.request.LANGUAGE_CODE
            self.language = self.request.query_params.get("lang", lang).lower()

        # cache
        if kwargs.get("cache_key"):
            cache_key = kwargs["cache_key"]
            if cache.get(cache_key):
                data = cache.get(cache_key)
            else:
                serializer = self.prepare_data(**kwargs)
                data = serializer.data
                cache.set(cache_key, data)
        else:
            serializer = self.prepare_data(**kwargs)
            data = serializer.data

        results = self.paginate_queryset(data)
        response = {
            "data": results,
            "language": self.language,
        }
        return self.get_paginated_response(response)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"language": self.language})
        return context


class ApiEndpointDetail(ApiEndpointList):
    def get(self, obj, **kwargs):
        self.language = str(self.request.query_params.get("lang", "null")).lower()
        if self.language == "null":
            self.language = self.request.LANGUAGE_CODE

        queryset = self.get_queryset()
        if queryset is not None and len(queryset) > 0:
            serializer = self.get_serializer(queryset[0], many=False)
            return Response(
                {
                    "results": serializer.data,
                    "labels": encode_labels(serializer.data, self.language),
                }
            )

        return Response({"results": {}, "labels": {}})


class ApiEndpointListSupport(ApiEndpointList):
    pagination_class = None
    permission_classes = [permissions.AllowAny]
    allowed_methods = ("GET",)

    def get(self, obj, **kwargs):
        self.language = str(self.request.query_params.get("lang", "null")).lower()
        if self.language == "null":
            self.language = self.request.LANGUAGE_CODE

        queryset = self.get_queryset()

        if queryset is not None and len(queryset) > 0:
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "results": serializer.data,
                    "labels": encode_labels(list(serializer.data)[0], self.language),
                }
            )

        return Response({"results": {}, "labels": {}})
