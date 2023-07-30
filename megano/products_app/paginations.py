from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """Пагинация"""
    page_size = 1
    page_query_param = 'currentPage'
    max_page_size = 10

    def get_paginated_response(self, data) -> Response:
        return Response({
            'items': data,
            'lastPage': self.page.paginator.count,
            'currentPage': self.page.number,
            'totalCount': self.page.paginator.count,

        })