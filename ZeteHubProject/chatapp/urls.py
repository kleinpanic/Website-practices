from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_channels_view, name='list_channels'),  # List all channels
    path('create_channel/', views.create_channel_view, name='create_channel'),  # Admin-only channel creation
    path('<str:channel_name>/', views.chatroom_view, name='chatroom'),  # Specific chatroom by name
    path('<str:channel_name>/send_message/', views.send_message, name='send_message'),  # Send message in a chatroom
]
