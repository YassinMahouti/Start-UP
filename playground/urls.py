from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.say_hello),
    path('', views.index, name='index'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('registration/', views.registrationPage, name='registration'),
    path('user/', views.userPage, name="user-page"),
    path('subscriptions/', views.subsPage, name='subshome'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path('webhook/', views.stripe_webhook),
]
