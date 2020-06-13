from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AccountForm
from .models import Account, Keyword
from .serializers import AccountSerializer

# Create your views here.


class CreateAccount(CreateView):
    # TODO
    # - Add autocomplete field for bank section
    model = Account
    form_class = AccountForm
    template_name = "accounts/edit_account.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["message"] = "Add Account"
        return ctx

    def form_valid(self, form):
        form.save(commit=False)
        # print(self.request.user.id)
        form.instance.user = self.request.user
        form.save()
        return redirect("accounts:account_list")


class EditAccount(UserPassesTestMixin, UpdateView):  # Note that we are using UpdateView and not FormView
    model = Account
    form_class = AccountForm
    template_name = "accounts/edit_account.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["message"] = "Update Account"
        return ctx

    def test_func(self):
        auth_user = self.get_object().user
        return self.request.user == auth_user

    def form_valid(self, form):
        # custom here if needed
        return super().form_valid(form)


def delete_account(request, slug):
    account = Account.objects.get(uuid=slug)
    account.delete()
    messages.add_message(request, messages.INFO, "Account successfully deleted")
    return redirect("accounts:account_list")


class AccountView(UserPassesTestMixin, DetailView):
    model = Account

    def test_func(self):
        auth_user = self.get_object().user
        return self.request.user == auth_user


class AccountList(LoginRequiredMixin, ListView):
    # TODO
    # figure out slug for viewing an account. uuid of sorts
    model = Account

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.GET.get("categories"):  # show categories instead of normal accounts
            ctx["categories"] = True
        return ctx


def account_ajax(request):
    if request.GET.get("categories"):
        accounts = [x for x in request.user.accounts.all() if x.is_category]
    else:
        accounts = [x for x in request.user.accounts.all() if not x.is_category]
    response = AccountSerializer(accounts, many=True)
    return JsonResponse(response.data, safe=False)


class KeywordList(ListView):
    model = Keyword
    context_object_name = "keywords"
