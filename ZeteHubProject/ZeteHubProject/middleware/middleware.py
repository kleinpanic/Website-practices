from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that ensures every user is authenticated before accessing any view,
    except the login and signup views.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs the user can access without authentication
        allowed_paths = [reverse('login'), reverse('signup')]

        # If user is not authenticated and tries to access restricted pages
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('login')

        response = self.get_response(request)
        return response
