from django.urls import path
from .views import register, confirm_registration

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm-registration/', confirm_registration, name='confirm_registration'),
]
