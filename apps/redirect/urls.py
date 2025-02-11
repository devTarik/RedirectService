from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.redirect.views import PrivateRedirectViewSet, PublicRedirectViewSet, UrlViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"public", PublicRedirectViewSet, basename="public-redirect")
router.register(r"private", PrivateRedirectViewSet, basename="private-redirect")


urlpatterns = [
    path("redirect/", include(router.urls)),
    path("url/", UrlViewSet.as_view({"post": "post"}), name="create-redirect"),
    path("url/<str:redirect_identifier>", UrlViewSet.as_view({"put": "put", "delete": "delete"}), name="item_redirect"),
]
