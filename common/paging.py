# common/paging.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings


# Extend this to add pagination to APIViews
class PagingAPIView(APIView):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_paginated_list_response(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request':request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
