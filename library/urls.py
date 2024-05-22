from . import views
from django.urls import path

app_name = 'library'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about-page'),
]
