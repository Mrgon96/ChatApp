from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserInfoForm, UserForm
# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def special(request):
    return HttpResponse("You are Logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_registration(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            registered = True
            user.is_active = True
            user.is_staff =True

        else:
            print(user_form.errors, user_info_form.errors)
    else:
        user_form = UserForm
        user_info_form = UserInfoForm

    context = {
        "user_form": user_form,
        "user_info_form": user_info_form,
        "registered": registered

    }
    return render(request, 'registration.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive")

        else:
            print("Login Failed")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid Login Details")

    else:
        return render(request, 'login.html', {})


