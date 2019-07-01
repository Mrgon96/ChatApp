from django.conf.urls import url
from users import views
# SET THE NAMESPACE!
app_name = 'users'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.user_registration,name='register'),
    url(r'^login/$',views.user_login,name='user_login'),
]