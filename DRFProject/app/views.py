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