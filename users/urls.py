from django.urls import path

# models
from .views import (
    UsersAPIView,
    CreateUserAPIView,
    UpdateUserAPIView,
    UserAPIView,
    DeleteUserAPIView,
    UpdatePasswordView
)

urlpatterns = [
    path("", UsersAPIView.as_view(), name="users"),
    path("create-user", CreateUserAPIView().as_view(), name="create-user"),
    path("<str:user_id>", UserAPIView.as_view(), name="user"),
    path("update-user/<str:user_id>",
         UpdateUserAPIView.as_view(), name="update-user"),
    path("delete-user/<str:user_id>",
         DeleteUserAPIView.as_view(), name="delete-user"),
    path("update-password/<str:user_id>",
         UpdatePasswordView.as_view(), name="update-password")
]
