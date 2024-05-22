from . import views
from django.contrib import admin
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
]
