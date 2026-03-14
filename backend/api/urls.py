from django.urls import path
from .views import register, login, request_password_reset, confirm_password_reset, dashboard_summary, create_product, create_receipt, create_delivery

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('password-reset/request/', request_password_reset),
    path('password-reset/confirm/', confirm_password_reset),
    path('dashboard/summary/', dashboard_summary),
    path('products/create/', create_product),
    path('receipts/create/', create_receipt),
    path('deliveries/create/', create_delivery),
]