import os
import requests
from dotenv import load_dotenv

from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import UserLogInForm, UserSignUpForm


load_dotenv()

def handle_api_url(abstract_path: str):
    return str(os.getenv('API_URL') + abstract_path)


def index_view(request):
    context = {
        "message": "This is Homepage"
    }
    return render(request, 'index.html', context=context)


def user_view(request, token: str):
    if request.method == 'POST':
        form_data = request.POST.dict()
        cleaned_form_data = {}

        for k, v in form_data.items():
            if v == '' or k == 'csrfmiddlewaretoken': continue
            else: cleaned_form_data[k] = v

        response = requests.put(handle_api_url("api/v1/user/"), data=cleaned_form_data, cookies={'jwt': token}).json()
        return redirect(reverse('user_view', kwargs={'token': token}))
    else:
        user = requests.get(handle_api_url("api/v1/user/"), cookies={'jwt': token}).json()
        context = {
            "token": token,
            "fields": [
                {"label": "Username", "value": user['username']}, 
                {"label": "Email", "value": user['email']}, 
                {"label": "Address", "value": user['address']}
            ]
        }
        return render(request, 'user.html', context=context)


def handle_user_delete_data(request, token: str, item_field: str):
    print(item_field)
    item_field = item_field.lower()
    payload = {
        'address': ''
    }
    if item_field in ['username', 'email']:
        messages.error("Can't set required field to null")
        return redirect(reverse('user_view', kwargs={'token': token}))
    user = requests.put(handle_api_url("api/v1/user/"), data=payload, cookies={'jwt': token}).json()

    return redirect(reverse('user_view', kwargs={'token': token}))


def login_view(request):
    form = UserLogInForm()

    if request.method == 'POST':
        form = UserLogInForm(request.POST)

        if form.is_valid():
            response = requests.post(handle_api_url("api/v1/login/"), data={'email': form.cleaned_data.get('email'), 'password': form.cleaned_data.get('password')})
            token = response.cookies.get('jwt')
            if token:
                return redirect(reverse('user_view', kwargs={'token': response.cookies.get('jwt')}))
            else:
                messages.error(request, response.json()['detail'])
                return redirect(reverse('login_view'))
    context = {
        "form": form
    }
    return render(request, 'login.html', context=context)


def signup_view(request):
    form = UserSignUpForm()

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 != password2:
                messages.error(request, 'Password confirmation failed')
                return redirect(reverse('login_view'))
            else:
                payload = {
                    "email": email, 
                    "username": username, 
                    "address": address, 
                    "password": password2
                }
                response = requests.post(handle_api_url("api/v1/register/"), data=payload)
                if response.ok:
                    messages.success(request, 'Account created')
                    return redirect(reverse('login_view'))
    context = {
        "form": form
    }
    return render(request, 'signup.html', context=context)


def logout_view(request, token: str):
    response = requests.post(handle_api_url("api/v1/logout/"), cookies={'jwt': token}).json()
    return redirect(reverse('login_view'))
