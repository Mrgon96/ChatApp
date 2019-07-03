from django.conf.urls import url
from users import views
from django.urls import path
# SET THE NAMESPACE!
app_name = 'users'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.user_registration,name='register'),
    url(r'^login/$',views.user_login,name='user_login'),
    url(r'^logout/$',views.user_logout,name='user_logout'),
    url(r'^users/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]