from django.shortcuts import render, redirect
from .models import UserCredentials
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import hashlib
import random
import string

# Helper function for hashing passwords
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Helper function to generate random salt
def generate_salt(length=16):
    """Generates a random salt."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('home')
        else:
            # Invalid login
            messages.error(request, 'Invalid username or password.')

    return render(request, 'authapp/login.html')

def signup_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Check if the user's phone number and name exist in the database
            preapproved_user = UserCredentials.objects.get(phone_number=phone_number, first_name=first_name, last_name=last_name)
            messages.error(request, 'User already exists.')
            return redirect('login')

        except UserCredentials.DoesNotExist:
            # Create new user, but no salt field required anymore
            new_user = UserCredentials.objects.create(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            new_user.set_password(password)  # Use set_password to hash the password
            new_user.save()

            # Automatically log in the user after signup
            login(request, new_user)
            return redirect('home')

    return render(request, 'authapp/signup.html')

# Example placeholder for a restricted view (Home page)
@login_required
def home_view(request):
    return HttpResponse(f"Welcome to your homepage, {request.session.get('username')}!")
