from django.shortcuts import render
from transactions.models import Transaction
from accounts.models import Account
from users.models import User
# Create your views here.


def home(request):
    return render(request, 'home/home.html')

def dashboard(request):
    ctx = {}
    all_accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.all()
    categories = set([obj.category for obj in transactions])
    category_stats = [{category: len(Transaction.objects.filter(category=category))} for category in categories] 
    net_worth = 0
    for account in all_accounts:
        net_worth += account.balance
    ctx['net_worth'] = net_worth
    ctx['accounts'] = all_accounts
    ctx['transactions'] = transactions
    ctx['category_stats'] = category_stats
    return render(request, 'home/dashboard.html', ctx)