from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    """Home view that is restricted to logged-in users."""
    return render(request, 'homeapp/home.html')

@login_required
def profile_view(request):
    """View for displaying the user's profile."""
    return render(request, 'homeapp/profile.html')
