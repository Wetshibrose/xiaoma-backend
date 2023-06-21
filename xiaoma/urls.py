
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("audits/", include("audits.urls")),
    path("countries/", include("countries.urls")),
    path("users/", include("users.urls")),
    path("auth/", include("authentication.urls")),
]
