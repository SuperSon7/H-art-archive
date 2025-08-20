from rest_framework.routers import DefaultRouter

from .views import PublicArtworkViewset

router = DefaultRouter()
router.register(r"", PublicArtworkViewset, basename="artworks")
# router.register(r'my-artworks', MyArtworkViewSet, basename='my-artwork')
# router.register(r'admin', AdminArtworkViewSet, basename='admin-artwork')
urlpatterns = []

urlpatterns += router.urls
