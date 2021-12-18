from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.say_hello),
    path('', views.index, name='index'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('registration/', views.registrationPage, name='registration'),
]
