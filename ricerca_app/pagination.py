import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ricerca_app.utils import encode_labels
from django.utils.encoding import force_str


class UnicalStorageApiPaginationList(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 250

    def url_refactor(self, url):
        pattern = re.compile(r"https?://")
        return pattern.sub('//', url) if url else None

    def get_paginated_response(self, data):
        return Response({
            'next':  self.url_refactor(self.get_next_link()),
            'previous': self.url_refactor(self.get_previous_link()),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'results': data['data'],
            'labels': encode_labels(data)
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'format': 'int32',
                    'example': 123,
                },
                # 'page': {
                #     'type': 'integer',
                #     'format': 'int32',
                #     'example': 123,
                # },
                # 'page_size': {
                #     'type': 'integer',
                #     'format': 'int32',
                #     'example': 123,
                # },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?page=400'
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?page=200'
                },
                'results': schema,

            },
        }

    def get_schema_operation_parameters(self, view):
        parameters = [
            {
                'name': self.page_query_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.page_query_description),
                'schema': {
                    'type': 'integer',
                    'format': 'int32'
                },
            },
        ]
        if self.page_size_query_param is not None:
            parameters.append(
                {
                    'name': self.page_size_query_param,
                    'required': False,
                    'in': 'query',
                    'description': force_str(self.page_size_query_description),
                    'schema': {
                        'type': 'integer',
                        'format': 'int32'
                    },
                },
            )
        return parameters
