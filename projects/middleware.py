# myapp/middleware.py

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class SimplePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the session already has the password verified
        if not request.session.get('is_authenticated', False):
            # Check the URL to avoid redirect loops with the login page
            if request.path != reverse('password_login'):
                return redirect('password_login')
        
        response = self.get_response(request)
        return response