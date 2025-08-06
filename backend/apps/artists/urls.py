from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ArtistsProfileViewSet

router = DefaultRouter()
router.register(r'artists', ArtistsProfileViewSet, basename='artist')

urlpatterns = []

urlpatterns += router.urls