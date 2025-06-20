from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/', login_user, name="login"),
    path('wallet/', view_wallet_balance, name="wallet"),
    path('transfer/', transfer_amount, name="transfer"),
    path('transaction/', get_transaction, name="transaction"),
]