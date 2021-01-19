from django.urls import path

from .views import RegistrationView, LoginView, HomeView
from django.contrib.auth.views import LogoutView

app_name = 'main'

urlpatterns = [
    path('home', HomeView.as_view(), name="home"),
    path('register',RegistrationView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
]
