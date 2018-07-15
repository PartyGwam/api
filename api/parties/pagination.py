from rest_framework.exceptions import NotFound

from pg_rest_api.pagination import StandardPagination


class PartyAPIPagination(StandardPagination):
    page_size = 20

    def get_paginated_response(self, data):
        if not self.page.paginator.count:
            raise NotFound()
        return super(PartyAPIPagination, self).get_paginated_response(data)
