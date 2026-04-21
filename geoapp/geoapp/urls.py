from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('results/', views.results),
    path('history/', views.history),
]