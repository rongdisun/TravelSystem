from django.urls import path
from . import views

app_name = "area"

urlpatterns = [
    path('province-autocomplete/', views.ProvinceAutocomplete.as_view(), name='province-autocomplete'),
    path('city-autocomplete/', views.CityAutocomplete.as_view(), name='city-autocomplete'),
]
