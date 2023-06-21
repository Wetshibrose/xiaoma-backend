from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request


# permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions
from knox.auth import TokenAuthentication
from .permissions import IsOwnerPermission


# models
from .models import CustomUser, Gender, Country

# serializers
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
)


class UsersAPIView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerPermission)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, *args, **kwargs):
        try:
            users: list[CustomUser] = CustomUser.objects.filter(
                is_deleted=False)

        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializers = UserSerializer(users, many=True)
        return Response({"data": serializers.data}, status=status.HTTP_200_OK)


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data: dict = serializer.validated_data
        try:
            user: CustomUser = CustomUser.objects.create_user(
                email=data.get("email"),
                phone_number=data.get("phone_number"),
                password=data.get("password"),
                gender=data.get("gender"),
                cor=data.get("cor"),
            )
            serializer = UserSerializer(user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "An error occured while creating the user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAPIView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerPermission)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, user_id: str, *args, **kwargs):
        try:
            user: CustomUser = CustomUser.objects.get(id=user_id)
            if user.is_deleted:
                return Response({"error": "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request: Request, user_id: str, format=None, *args, **kwargs):
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

        data: dict = serializer.validated_data
        try:
            user: CustomUser = CustomUser.objects.get(id=user_id)
            user.email = data.get("email")
            user.phone_number = data.get("phone_number")
            user.gender = data.get("gender") if data.get(
                "gender") else user.gender
            user.cor = data.get("cor") if data.get("cor") else user.cor
            user.ratings = data.get("ratings") if data.get(
                "ratings") else user.ratings
            user.is_online = data.get("is_online") if data.get(
                "is_online") else user.is_online
            user.updated_at = timezone.now()
            user.save()
            serializer = UserSerializer(user)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": "Something went wrong when updating user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePasswordView(APIView):
    permission_classes = (IsAuthenticated | AllowAny,)

    def get_object(self, user_id: str):
        try:
            user: CustomUser = CustomUser.objects.get(id=user_id)
            if user.is_deleted:
                return None
            return user
        except Exception as error:
            return None

    def post(self, request: Request, user_id: str, *args, **kwargs):
        user = self.get_object(user_id=user_id)
        if not user:
            return Response({"error": "User with given id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        password: str = request.data.get("password")
        if not password:
            return Response({"error": "password field is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(f"password {password}")
            user.set_password(password)
            user.updated_at = timezone.now()
            user.save()
            return Response({"data": "Password changed successfully"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "Something happened when changing password"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MakeStaffAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id: str):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except Exception as error:
            return None

    def post(self, request: Request, user_id: str, *args, **kwargs):
        user = self.get_object(user_id=user_id)
        if not user:
            return Response({"error": "User with given id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        is_staff: bool = request.data.get("is_staff")
        if is_staff is None:
            return Response({"error": "password field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            user.is_staff = is_staff
            user.updated_at = timezone.now()
            user.save()
            return Response({"data": "Password changed successfully"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "Something happened when changing password"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def delete(self, request: Request, user_id, *args, **kwargs):
        try:
            user: CustomUser = CustomUser.objects.get(id=user_id)
            if user.is_deleted:
                return Response({"error": "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

            user.is_deleted = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
