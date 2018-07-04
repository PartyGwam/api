from rest_framework import pagination
from rest_framework.response import Response


class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'data': data,
            'paging': {
                'previous': self.get_previous_link(),
                'next': self.get_next_link(),
            }
        })
