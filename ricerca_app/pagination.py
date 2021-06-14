import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ricerca_app.utils import encode_labels


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
