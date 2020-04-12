import copy
import csv
import decimal
import html
import io
from datetime import datetime
from itertools import zip_longest

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.models import Account

from .forms import TransactionForm
from .models import Ledger, Transaction
from .serializers import TransactionSerializer

# Create your views here.

# Group by 3, the number of fields for each ledger. Produces list of tuples where
# each tuple contains info for each ledge. Default n=3, the number of fields per user
def grouper(iterable, n=3, fillvalue=""):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def transaction_ajax(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get
    ledgers = Ledger.objects.filter(account__uuid=get("uuid"))
    transactions = set([x.transaction for x in ledgers])
    response = TransactionSerializer(transactions, many=True, uuid=get("uuid"))
    return JsonResponse(response.data, safe=False)


def transaction_form(request):
    ctx = {}
    if request.method == "POST":
        data = request.POST
        print(data)
        # filter here - get ledger information fields
        field_dict = list(filter(lambda x: "ledger_" in x, request.POST))
        grouped_fields = list(grouper(field_dict))

        # Transaction info
        date = data["date"]
        notes = data["notes"]
        name = data["name"]
        transaction = Transaction(date=datetime.strptime(date, "%m/%d/%Y"), notes=notes, name=name)
        transaction.save()

        print(grouped_fields)
        for group in grouped_fields:
            # Ledger Account info
            account = Account.objects.get(name=data[group[0]])  # lookup by name
            memo = data[group[1]]
            amount = data[group[2]]

            new_ledger = Ledger(account=account, memo=memo, amount=amount, transaction=transaction)
            new_ledger.save()

        return redirect("accounts:view", slug=data["account_uuid"])

    else:
        # initialize new form
        uuid = request.GET.get("account")
        form = TransactionForm(uuid=uuid)
        ctx["message"] = "Create a Transaction"

    # grab additional visitor row html as a string for template context
    row = html.unescape(render_to_string("transactions/row.html").replace("\n", ""))
    ctx["form"] = form
    ctx["row"] = row
    ctx["rm_jquery"] = True  # weird issue with this and autocomplet init
    return render(request, "transactions/edit_transaction.html", ctx)


def transaction_view(request, account, transaction):
    account_obj = Account.objects.get(uuid=account)
    transaction = Transaction.objects.get(uuid=transaction)
    ledgers = transaction.ledgers.all()
    _sum = 0
    for ledger in ledgers:
        _sum += ledger.amount if str(ledger.account_id) == str(account) else 0
    ctx = {}
    ctx["sum"] = _sum
    ctx["transaction"] = transaction
    ctx["ledgers"] = [x for x in ledgers if str(x.account_id) != str(account)]
    ctx["account"] = account_obj
    return render(request, "transactions/transaction_view.html", ctx)


def transaction_delete(request, slug):
    obj = Transaction.objects.get(uuid=slug)
    account_uuid = obj.account.uuid
    obj.account.balance -= obj.amount
    obj.account.save()
    obj.delete()
    return redirect("accounts:view", slug=account_uuid)
