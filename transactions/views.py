import copy
import csv
import decimal
import io
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.models import Account

from .forms import TransactionForm
from .models import Transaction, Category
from .serializers import TransactionSerializer

# Create your views here.


def transaction_ajax(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get
    transactions = Transaction.objects.filter(account__uuid=get("uuid"))
    response = TransactionSerializer(transactions, many=True)
    return JsonResponse(response.data, safe=False)


""" Server side processing example: """
# def drawing_list_ajax(request):
#     if request.method == "POST":
#         get = request.POST.get
#     else:
#         get = request.GET.get

#     start = int(get('start'))
#     length = int(get('length'))
#     end = start + length
#     search = get('search[value]')
#     order_column_index = int(get('order[0][column]'))
#     order_direction = get('order[0][dir]')
#     order_column_name = get('columns[{}][name]'.format(order_column_index))
#     # print('{}, {}'.format(order_column_name, order_direction))
#     if order_direction == "asc":
#         drawings = Drawing.objects.order_by('{}'.format(order_column_name))
#     else:
#         drawings = Drawing.objects.order_by('-{}'.format(order_column_name))
#     records_total = len(drawings)

#     if search:
#         query = (Q(number__icontains=search) | Q(description__icontains=search) |
#                     Q(program_drawing__name__icontains=search) | Q(drawnby__name__icontains=search))
#         drawings = drawings.filter(query)

#     records_filtered = len(drawings)
#     drawings = drawings[start:end]
#     # drawing_qs = DrawingSerializer.setup_eager_load(drawings) # eager load is incompatible with serverside
#     serializer = DrawingSerializer(drawings, many=True)
#     response = {
#         "draw": int(get('draw')),
#         "recordsTotal": records_total,
#         "recordsFiltered": records_filtered,
#         "data": serializer.data,
#     }

#     return JsonResponse(response, safe=False)


class TransactionView(DetailView):
    model = Transaction

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["account_uuid"] = self.object.account.uuid
        return ctx


class CreateTransaction(CreateView):
    # TODO
    # - Add autocomplete field for category section
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/edit_transaction.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["message"] = "Add Transaction"
        return ctx

    def form_valid(self, form):
        if self.request.method == "POST":
            get = self.request.POST.get
        else:
            get = self.request.GET.get

        form.save(commit=False)
        uuid = self.request.GET["account"]
        form.instance.account = Account.objects.get(uuid=uuid)
        form.instance.category = form.cleaned_data["category"]
        form.instance.date = datetime.strptime(get("date"), "%m/%d/%Y")
        form.instance.notes = get("notes")
        form.save()
        return redirect("accounts:view", slug=uuid)


class TransactionEdit(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/edit_transaction.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["message"] = "Edit Transaction"
        return ctx

    def form_valid(self, form):
        # access old values before save
        # https://stackoverflow.com/questions/56305992/how-to-access-previous-value-of-a-field-in-django-model-form-before-save
        obj = Transaction.objects.get(pk=form.instance.pk)
        prev_obj = copy.copy(obj)
        # here you can access any field of your previous object related to that instance.

        # subtract old amount value from account balance to accuratley reflect balance after edit
        form.instance.account.balance -= prev_obj.amount
        # form.save below takes care of saving the account instance as well
        form.save()
        return redirect("transactions:view", slug=self.object.uuid)


def transaction_delete(request, slug):
    obj = Transaction.objects.get(uuid=slug)
    account_uuid = obj.account.uuid
    obj.account.balance -= obj.amount
    obj.account.save()
    obj.delete()
    return redirect("accounts:view", slug=account_uuid)


def transaction_import(request):
    if request.method == "POST" and request.FILES.get("import"):
        get = request.POST.get
        account = Account.objects.filter(uuid=get("uuid")).first()
        if request.user != account.user:
            raise PermissionDenied()

        csvfile = request.FILES["import"]
        decoded_file = csvfile.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)

        fieldnames = [
            "Transaction Number",
            "Date",
            "Description",
            "Memo",
            "Amount Debit",
            "Amount Credit",
            "Balance",
            "Check Number",
            "Fees",
            "Principal",
            "Interest",
        ]
        csv_reader = csv.DictReader(io_string, delimiter=",", quotechar='"', fieldnames=fieldnames)
        line_count = 0
        attempted = 0  # keep track of attempted saves
        duplicates = []
        for line in csv_reader:
            if line_count not in [0, 1, 2, 3]:
                if line.get("Amount Debit"):
                    amount = decimal.Decimal(line.get("Amount Debit"))
                else:
                    amount = decimal.Decimal(line.get("Amount Credit"))
                new_transaction = Transaction(
                    account=account,
                    name=line["Memo"],
                    amount=amount,
                    category=line["Description"],
                    date=datetime.strptime(line["Date"], "%m/%d/%Y"),
                    notes="Imported on {} from csv".format(datetime.today().strftime("%m/%d/%Y")),
                )
                try:
                    attempted += 1
                    new_transaction.save()
                except IntegrityError:
                    duplicates.append(new_transaction)
            line_count += 1
        if duplicates:
            if len(duplicates) == attempted:
                messages.add_message(
                    request,
                    messages.INFO,
                    "ATTENTION: No new transactions added. All attempted transactions were duplicates. Have you \
                        uploaded this file before?",
                    extra_tags="danger",
                )
            else:
                messages.add_message(
                    request, messages.INFO, "Transactions successfully imported!", extra_tags="success"
                )
                messages.add_message(
                    request, messages.INFO, "WARNING: Some duplicates were ignored.", extra_tags="warning",
                )
        else:
            messages.add_message(request, messages.INFO, "Transactions successfully imported!", extra_tags="success")
        return redirect("accounts:view", slug=get("uuid"))
    else:
        uuid = request.GET["uuid"]
        account = Account.objects.filter(uuid=uuid).first()
        if request.user != account.user:
            raise PermissionDenied()
        ctx = {}
        ctx["uuid"] = uuid
        return render(request, "transactions/import.html", ctx)
