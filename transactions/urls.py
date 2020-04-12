from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("ajax/", views.transaction_ajax, name="ajax"),
    path("transaction_form/", views.transaction_form, name="transaction_form"),
    path("transactions/<account>/<transaction>/", views.transaction_view, name="transaction_view"),
]
