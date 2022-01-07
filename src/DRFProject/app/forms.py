from django import forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)
    address = forms.CharField(max_length=150, required=False)
    username = forms.CharField(max_length=120, required=True)
    password1 = forms.CharField(max_length=120, required=True)
    password2 = forms.CharField(max_length=120, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'password1', 'password2']


class UserLogInForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(max_length=120, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
