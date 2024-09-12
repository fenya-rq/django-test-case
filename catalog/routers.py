from django.urls import path
from rest_framework import routers

from .views import CatalogViewSet

router = routers.DefaultRouter()
router.register(r'goods', CatalogViewSet)
