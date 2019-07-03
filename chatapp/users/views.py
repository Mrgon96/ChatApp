from webbrowser import get
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserInfoForm, UserForm
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activate_token
from django.core.mail import EmailMessage



def index(request):
    return render(request, 'index.html')

# @login_required
# def special(request):
#     return HttpResponse("You are Logged in")

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('login.html'))

def user_registration(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            registered = True

            current_site = get_current_site(request)
            subject = "Activate Your ChatApp Account"
            message = render_to_string('account_activate.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                           'token': account_activate_token.make_token(user)
                                       })
            from_email = settings.EMAIL_HOST_USER
            to_send = [user.email]
            # email = EmailMessage(subject, message, to_send)
            # email.send()
            send_mail(subject, message, from_email, to_send, fail_silently=False)

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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


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


