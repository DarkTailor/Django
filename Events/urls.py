from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_events, name='list_events'),
    path('add/', views.add_events, name='add_events'),
    path('create/', views.create_event, name='create_event'),
    path('<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('<int:pk>/delete/', views.delete_event, name='delete_event'),
    # Add other URL patterns as needed
]
