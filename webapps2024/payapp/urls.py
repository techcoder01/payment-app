# payapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('request-money/', views.request_money, name='request-money'),
    path('send-money/', views.send_money, name='send-money'),
    path('send-money-success/', views.send_money_success, name='send-money-success'),
    path('request-money-success/', views.request_money_success, name='request-money-success'),
    path('send-money-confirm/', views.send_money_confirm, name='send-money-confirm'),
    path('request-money-confirm/', views.request_money_confirm, name='request-money-confirm'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('payment_methods/', views.payment_methods, name='payment-methods'),
    path('delete_card/', views.delete_card, name='delete_card'),
    path('delete_bank_account/', views.delete_bank_account, name='delete_bank_account'),
]
