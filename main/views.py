from rest_framework import views, status
from rest_framework.response import Response
from . import models as main_models
from . import serializers as main_serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny



class CustomPagination(PageNumberPagination):
    allow_empty_first_page = True
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

class PhotoAPIView(views.APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = main_serializers.PhotoSerializer

    def get(self, request):
        paginator = self.pagination_class()
        queryset = main_models.Photo.objects.all().order_by('-id')[:15]
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)