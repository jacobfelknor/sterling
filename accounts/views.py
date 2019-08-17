from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AccountForm
from .models import Account
from .serializers import AccountSerializer

# Create your views here.

class CreateAccount(CreateView):
    # TODO
    # - Add autocomplete field for bank section
    model = Account
    form_class = AccountForm
    template_name = 'accounts/edit_account.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['message'] = "Add Account"
        return ctx

    def form_valid(self, form):
        form.save(commit=False)
        # print(self.request.user.id)
        form.instance.user = self.request.user
        form.save()
        return redirect('accounts:account_list')

class EditAccount(UpdateView): #Note that we are using UpdateView and not FormView
    model = Account
    form_class = AccountForm
    template_name = "accounts/edit_account.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['message'] = "Update Account"
        return ctx

    # def get_success_url(self, *args, **kwargs):
    #     return reverse("accounts.views.view_account")

class AccountList(ListView):
    # TODO
    # figure out slug for viewing an account. uuid of sorts
    model = Account

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class AccountView(DetailView):
    model = Account

def account_ajax(request):
    accounts = request.user.accounts.all()
    response = AccountSerializer(accounts, many=True)
    return JsonResponse(response.data, safe=False)
