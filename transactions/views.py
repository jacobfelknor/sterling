from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import Account

from .forms import TransactionForm, DateForm
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.

def transaction_ajax(request):
    if request.method == "POST":
        get = request.POST.get
    else:
        get = request.GET.get

    transactions = Transaction.objects.filter(account__uuid=get('uuid'))
    response = TransactionSerializer(transactions, many=True)
    return JsonResponse(response.data, safe=False)


class CreateTransaction(CreateView):
    # TODO
    # - Add autocomplete field for category section
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/edit_transaction.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['message'] = "Add Transaction"
        ctx['date_form'] = DateForm
        return ctx

    def form_valid(self, form):
        form.save(commit=False)
        uuid = self.request.GET['account']
        form.instance.account = Account.objects.get(uuid=uuid)
        form.save()
        return redirect('accounts:view', slug=uuid)


class TransactionView(DetailView):
    model = Transaction
