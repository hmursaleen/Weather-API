from django.urls import path
from . import views

urlpatterns = [
    path('weather/<str:city_name>/', views.WeatherView.as_view(), name='weather'),
]
