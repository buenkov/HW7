from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = 'simple_sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'simple_sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name = 'simple_sign/signup.html'),
         name='signup'),
]