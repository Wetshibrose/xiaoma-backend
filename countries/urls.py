from django.urls import path

from .views import (
    CountriesAPIView,
    CountryAPIView,
    CreateCountryAPIView,
)

urlpatterns = [
    path("", CountriesAPIView.as_view(), name="countries"),
    path("create-country", CreateCountryAPIView.as_view(), name="create-country"),
    path("<str:country_id>", CountryAPIView.as_view(), name="country"),
]
