from rest_framework import serializers

from .models import Country


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "country_code",
            "created_at",
        )


class CreateCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "country_code",
            "created_at",
        )
        read_only = ("id", "created_at")


class UpdateCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "country_code",
            "updated_at",
        )
        read_only = ("id", "updated_at")
