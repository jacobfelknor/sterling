from django.urls import path

from . import forms, views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountList.as_view(), name='account_list'),
    path('<pk>', views.AccountView.as_view(), name='view'),
    path('<pk>/edit/', views.EditAccount.as_view(), name='edit'),
    path('create/', views.CreateAccount.as_view(), name='create_account'),
    path('ajax/', views.account_ajax, name='account_ajax'),
]