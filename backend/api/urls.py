from django.urls import path
from .views import register, login, request_password_reset, confirm_password_reset

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('password-reset/request/', request_password_reset),
    path('password-reset/confirm/', confirm_password_reset),

]