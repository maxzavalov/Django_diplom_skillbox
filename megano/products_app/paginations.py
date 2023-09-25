from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'currentPage'
    max_page_size = 10

    def get_paginated_response(self, data) -> Response:
        return Response({
            'items': data,
            'lastPage': self.page.paginator.count,
            'currentPage': self.page.number,
            'totalCount': self.page.paginator.count,

        })