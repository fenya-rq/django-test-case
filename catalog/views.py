from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import GoodsSerializer

from .models import Goods


class CatalogViewSet(ReadOnlyModelViewSet):

    permission_classes = [AllowAny]
    queryset = Goods.objects.prefetch_related('images', 'parameters').all()
    serializer_class = GoodsSerializer
