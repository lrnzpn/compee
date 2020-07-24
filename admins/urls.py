from django.urls import path
from .views import MainDashboard

urlpatterns = [
    path('', MainDashboard, name='main-dash')
]