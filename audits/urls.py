from django.urls import path

from .views import (
    AuditsAPIView,
)
urlpatterns = [
    path("", AuditsAPIView.as_view(), name="audits"),
]
