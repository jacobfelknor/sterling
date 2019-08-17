from django.forms import ModelForm
from .models import Account

# Create the form class.
class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'number', 'bank', 'account_type', 'notes']

    # def save(self):
    #     account = 

    #     return account
