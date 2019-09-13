from django.urls import path

from . import views

app_name = 'transactions'

urlpatterns = [
    path('ajax/', views.transaction_ajax, name='ajax'),
    path('create/', views.CreateTransaction.as_view(), name='create'),
    path('view/<slug>', views.TransactionView.as_view(), name='view'),
]