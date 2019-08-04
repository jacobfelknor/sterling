from django.urls import path

from . import forms, views

app_name = 'accounts'

urlpatterns = [
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('signup/',views.UserSignUpView.as_view(), name='signup'),
    path('password/', forms.change_password, name='change_password'),
    path('<username>/view/', views.view_account, name='view_account'),
    path('<username>/edit-account/', views.EditUserAccountView.as_view(), name='edit_info'),
]