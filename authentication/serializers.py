from django.contrib.auth import authenticate
from rest_framework import serializers

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(required=False, allow_null=True)
    otp = serializers.CharField(required=False, allow_null=True)

    def validate(self, attrs: dict):
        email_value: str = attrs.get("email")
        phone_number_value: str = attrs.get("phone_number")

        if not email_value and not phone_number_value:
            raise serializers.ValidationError(
                "Either Email or phone number needs to be provided", code=400)

        password_value = attrs.get("password")
        otp_value = attrs.get("otp")

        if not password_value and not otp_value:
            raise serializers.ValidationError(
                "Provide either password or otp", code=400)

        if not CustomUser.objects.filter(email=email_value).exists():
            raise serializers.ValidationError(
                detail="Email or password doesn't exists", code=400)

        if email_value and password_value:
            user = authenticate(request=self.context.get(
                "request"), email=email_value, password=password_value,)
        elif phone_number_value and password_value:
            user_for_email = CustomUser.objects.filter(
                phone_number=phone_number_value)
            if not user_for_email.exists():
                raise serializers.ValidationError(
                    detail="Email or password doesn't exists", code=400)
            user_email = user_for_email.first().email
            user = authenticate(request=self.context.get(
                "request"), email=user_email, password=password_value,)
        else:
            pass

        if not user:
            raise serializers.ValidationError(
                detail="Wrong credentials have been given", code=400)

        attrs["user"] = user
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class CreateGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        queryset=Permission.objects.all(),
        slug_field="codename",
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "permissions",
        )
        read_only = ("id",)

    def create(self, validated_data: dict):
        permissions_data = validated_data.pop("permissions")
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions_data)
        return group


class UpdateGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        queryset=Permission.objects.all(),
        slug_field="codename",
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Group
        fields = "__all__"

    def update(self, instance: Group, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        permissions_data = validated_data.get("permissions")

        for permission in permissions_data:
            instance.permissions.add(permission.id)

        return instance


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class CreatePermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        required=True
    )

    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "content_type",
            "codename",
        )
        read_only = ("id",)

    def create(self, validated_data: dict):
        permission = Permission.objects.create(
            name=validated_data.get("name"),
            codename=validated_data.get("codename"),
            content_type=validated_data.get("content_type"),
        )
        return permission


class UpdatePermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "content_type",
            "codename",
        )

    def update(self, instance: Permission, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        instance.codename = validated_data.get("codename", instance.codename)
        instance.content_type = validated_data.get(
            "content_type", instance.content_type)
        return instance


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = (
            "id",
            "app_label",
            "model",
        )
