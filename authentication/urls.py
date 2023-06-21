from django.urls import path

from .views import (
    LoginKnoxViews,
    GroupsAPIView,
    GroupAPIView,
    CreateGroupAPIView,
    UpdateGroupAPIView,
    PermissionsAPIView,
    PermissionAPIView,
    CreatePermissionAPIView,
    UpdatePermissionAPIView,
    ContentTypeAPIView
)
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    path("groups", GroupsAPIView.as_view(), name="groups"),
    path("create-group", CreateGroupAPIView.as_view(), name="create-group"),
    path("update-group/<int:pk>",
         UpdateGroupAPIView.as_view(), name="update-group"),
    path("groups/<int:pk>", GroupAPIView.as_view(), name="group"),
    path("permissions", PermissionsAPIView.as_view(), name="permissions"),
    path("permissions/<int:pk>", PermissionAPIView.as_view(), name="permissions"),
    path("create-permission", CreatePermissionAPIView.as_view(),
         name="create-permission"),
    path("update-permission/<int:pk>",
         UpdatePermissionAPIView.as_view(), name="update-permission"),
    path("apps", ContentTypeAPIView.as_view(), name="apps"),
    path("login", LoginKnoxViews.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="login"),
    path("logout-all", LogoutAllView.as_view(), name="login"),
]
