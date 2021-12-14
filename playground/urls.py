from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.say_hello),
    path('', views.index, name='index'),
    path('login/', views.login),
    path('registration/', views.registration),
]
