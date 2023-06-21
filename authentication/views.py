from django.contrib.auth.models import Group, Permission
from django.contrib.auth import login

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from knox.views import LoginView
from knox.auth import TokenAuthentication

from .serializers import (
    LoginSerializer,
    GroupSerializer,
    CreateGroupSerializer,
    PermissionSerializer,
    UpdateGroupSerializer,
    CreatePermissionSerializer,
    UpdatePermissionSerializer,
    ContentTypeSerializer,
)

from users.models import CustomUser
from django.contrib.contenttypes.models import ContentType


class LoginKnoxViews(LoginView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user: CustomUser = data["user"]
        if not user:
            return Response({"message": "user instance wasn't provided"}, status=status.HTTP_400_BAD_REQUEST)
        login(request=request, user=user)

        response = super().post(request, format=None)

        return Response(response.data, status=status.HTTP_200_OK)


class GroupsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, *args, **kwargs):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class GroupAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, pk: int, *args, **kwargs):
        if not pk:
            return Response({"error": "Group id should be provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({"error": "Group with given id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


class CreateGroupAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request: Request, *args, **kwargs):
        serializer = CreateGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            group = serializer.create(validated_data=data)
            return Response({"data": data}, status=status.HTTP_201_CREATED)
        except Exception as error:
            print(error)
            return Response({"error": "An error occured while creating role"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,)


class UpdateGroupAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, pk):
        try:
            group = Group.objects.get(pk=pk)
            return group
        except Exception as error:
            return None

    def put(self, request: Request, pk: int, *args, **kwargs):
        group = self.get_object(pk=pk)
        if group is None:
            return Response({"error": "Group with the id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateGroupSerializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class PermissionsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, *args, **kwargs):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class PermissionAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, pk: int, *args, **kwargs):
        if not pk:
            return Response({"error": "Permission id should be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            permission = Permission.objects.get(pk=pk)
            serializer = PermissionSerializer(permission)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({"error": "Permission with given id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


class CreatePermissionAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request: Request, *args, **kwargs):
        serializer = CreatePermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


class UpdatePermissionAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, pk: int):
        try:
            permission = Permission.objects.get(pk=pk)
            return permission
        except Exception as error:
            return None

    def put(self, request: Request, pk: int, *args, **kwargs):
        permission = self.get_object(pk=pk)
        if not permission:
            return Response({"error": "Permission with given id doesn't exist "}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePermissionSerializer(permission, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ContentTypeAPIView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, *args, **kwargs):
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
