from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from .models import CustomUser


class IsOwnerPermission(BasePermission):
    def has_permission(self, request: Request, view):
        user: CustomUser = request.user

        if user.is_superuser:
            return True

        if user.is_staff:
            if user.groups.filter(name="Admin").exists():
                return True
        return False

    def has_object_permission(self, request: Request, view, obj: CustomUser):
        print(f"request.user {request.user}")
        user: CustomUser = request.user

        if user.is_superuser:
            return True
        if user.id == obj.id:
            return True
        if user.is_staff:
            if user.groups.filter(name="Admin").exists():
                return True
        return False
