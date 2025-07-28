from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mulai-jelajah/', views.maps , name='mulai-jelajah'),
    path('city/<str:city_name>/', views.island, name='city-detail'),
    path('get-island/<str:pk>/', views.get_island),
    path('get-questions/<str:city_name>/', views.get_questions),
]
