from rest_framework.routers import DefaultRouter

from .views import ArtistProfileViewSet, ArtistsAdminViewSet

router = DefaultRouter()
router.register(r'', ArtistProfileViewSet, basename='artists')
router.register(r'admin', ArtistsAdminViewSet, basename='artists-admin')
urlpatterns = []

urlpatterns += router.urls
