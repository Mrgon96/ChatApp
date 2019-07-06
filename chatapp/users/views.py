from webbrowser import get
import jwt, json
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
from .models import UserInfo


from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, UserInfoSerializer


# This will return a list of books
@api_view(["GET"])
def book(request):
    books = ["Pro Python", "Fluent Python", "Speaking javascript", "The Go programming language"]
    return Response(status=status.HTTP_200_OK, data={"data": books})



def index(request):
    return render(request, 'build/index.html ')



def home(request):
    return render(request, 'home.html')
# @login_required
# def special(request):
#     return HttpResponse("You are Logged in")


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('login.html')


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

            payload = {'uid': user.id}

            encode=jwt.encode(payload, 'secret', algorithm='HS256')

            json.dump(encode)


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
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive")

        else:
            print("Login Failed")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid Login Details")

    else:
        return render(request, 'login.html', {})


# *************SERIALIZER FOR USERS FROM serializers.py***********************

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data)


class UserList(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = UserSerializerWithToken(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoList(APIView):
    def get(self, request, format=None):
        users = UserInfo.objects.all()
        serializer = UserInfoSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist:
            raise HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user=self.get_object(pk)
        serializer = UserInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user=self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
