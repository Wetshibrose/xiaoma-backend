from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .serializers import (
    CountrySerializers,
    CreateCountrySerializer,
    UpdateCountrySerializer,
)
from .models import Country


class CountriesAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request: Request, *args, **kwargs):
        countries = Country.objects.filter(is_deleted=False)

        if not countries.exists():
            return Response({"data": []}, status=status.HTTP_200_OK)

        serializer = CountrySerializers(countries, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class CountryAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, country_id: str, *args, **kwargs):
        if not country_id:
            return Response({"error": "country id should be passed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            country = Country.objects.get(id=country_id)
            if country.is_deleted:
                return Response({"error": "Country by that id is not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CountrySerializers(country)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": "Country by that id is not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateCountryAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request: Request, *args, **kwargs):
        serializer = CreateCountrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            country = Country.objects.create(
                name=data.get("name"),
                country_code=data.get("country_code")
            )
            if country.is_deleted:
                return Response({"error": "Country by that id is not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": "Country by that id is not found"}, status=status.HTTP_404_NOT_FOUND)
