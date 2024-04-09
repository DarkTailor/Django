# Donations/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_donations, name='list_donations'),
    path('add/', views.add_donation, name='add_donation'),
    path('create/', views.create_donation, name='create_donation'),
    # Add other URL patterns as needed
]
