from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("ajax/", views.transaction_ajax, name="ajax"),
    path("create/", views.CreateTransaction.as_view(), name="create"),
    path("import/", views.transaction_import, name="import"),
    path("<slug>/view/", views.TransactionView.as_view(), name="view"),
    path("<slug>/edit/", views.TransactionEdit.as_view(), name="edit"),
    path("<slug>/delete/", views.transaction_delete, name="delete"),
]
