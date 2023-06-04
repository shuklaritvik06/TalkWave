from django.contrib import admin
from django.urls import path, include
from .views import hello

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", hello),
    path("auth/", include("authentication.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/", include("chat.urls")),
]
