from django.shortcuts import render
from django.http import HttpResponse

def index_view(request):
    context = {
        "message": "This is Homepage"
    }
    return render(request, 'index.html', context=context)
    
def login_view(request):
    context = {
        "message": "This is login page"
    }
    return render(request, 'login.html', context=context)

def signup_view(request):
    context = {
        "message": "This is login page"
    }
    return render(request, 'signup.html', context=context)

def user_view(request):
    context = {
        "username": "Username",
        "fields": [
            {"label": "Username", "value":"Sarvesh"}, 
            {"label": "Email", "value":"email@email.com"}, 
            {"label": "Address", "value":"Some long address"}
        ]
    }
    return render(request, 'user.html', context=context)