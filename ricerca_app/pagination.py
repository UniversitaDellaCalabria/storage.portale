from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings


class UnicalStorageApiPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 250

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'results': data,
            'labels': self.encode_labels(data)
        })

    def encode_labels(self, data):
        labels = {}
        if len(data) > 0 and hasattr(settings, 'LABEL_MAPPING'):
            d = data[0]
            missing_key = False
            for key in d.keys():
                if key not in settings.LABEL_MAPPING.keys():
                    missing_key = True
                    break
                labels[key] = settings.LABEL_MAPPING[key]

            if missing_key:
                labels = {}

        return labels
