from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse


def index_view(request):
    return HttpResponse("API HOME")