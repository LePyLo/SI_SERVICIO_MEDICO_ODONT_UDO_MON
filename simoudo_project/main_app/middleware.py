from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class AutenticacionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return redirect('login') 
        return self.get_response(request)