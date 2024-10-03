from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('profile/', views.profile_view, name='profile'),  # User profile page
]
