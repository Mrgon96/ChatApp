from django import forms
from .models import UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class UserInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100,label="Last name")

    class Meta:
        model = UserInfo
        fields =[
            'first_name',
            'last_name',

        ]

