from django.urls import path
from database import views

urlpatterns = [
    path('', views.home, name = 'home'),
]