# api/urls.py
from django.urls import include, path
from rest_framework import routers

from .views import PersonViewSet, KeyViewSet

router = routers.DefaultRouter()
router.register(r'people', PersonViewSet, basename='person')
router.register(r'keys', KeyViewSet, basename='key')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
