from rest_framework import serializers

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

# models
from .models import CustomUser, Gender, Country


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "phone_number",
            "gender",
            "cor",
            "ratings",
            "is_active",
            "is_online",
            "is_staff",
            "created_at",
            "updated_at",
        )


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=14)
    password = serializers.CharField(min_length=8, max_length=32)
    gender = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.filter(is_deleted=False),
        required=False,
        allow_null=True
    )
    cor = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.filter(is_deleted=False),
        required=False,
        allow_null=True
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        allow_null=True
    )

    def validate(self, attrs: dict):
        email_value: str = attrs.get("email")
        phone_number_value: str = attrs.get("phone_number")

        if not email_value and not phone_number_value:
            raise serializers.ValidationError(
                "Either Email or phone number needs to be provided", code=400)

        if CustomUser.objects.filter(email=email_value).exists():
            raise serializers.ValidationError(
                detail="Email provided already exists", code=400)

        return attrs


class UpdateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=14)
    gender = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.filter(is_deleted=False),
        required=False,
        allow_null=True
    )
    cor = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.filter(is_deleted=False),
        required=False,
        allow_null=True
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        allow_null=True
    )
    ratings = serializers.DecimalField(
        decimal_places=1, max_digits=3, required=False)
    is_online = serializers.BooleanField(required=False)
