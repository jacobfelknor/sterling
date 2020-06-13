from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.AccountList.as_view(), name="account_list"),
    path("ajax/", views.account_ajax, name="account_ajax"),
    path("create/", views.CreateAccount.as_view(), name="create_account"),
    path("keywords/", views.KeywordList.as_view(), name="keyword_list"),
    path("<slug>/", views.AccountView.as_view(), name="view"),
    path("<slug>/edit/", views.EditAccount.as_view(), name="edit"),
    path("<slug>/delete/", views.delete_account, name="delete"),
]
