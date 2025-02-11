from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.redirect.urls")),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-create"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
