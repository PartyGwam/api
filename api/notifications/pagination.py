from rest_framework.exceptions import NotFound

from pg_rest_api.pagination import StandardPagination


class NotificationAPIPagination(StandardPagination):
    page_size = 20

    def get_paginated_response(self, data):
        if not self.page.paginator.count:
            raise NotFound('알림이 아무것도 오지 않았습니다.')
        return super().get_paginated_response(data)
