from django.forms import ModelForm
from .models import Account
from ajax_select.fields import AutoCompleteSelectMultipleField


# Create the form class.
class AccountForm(ModelForm):

    keywords = AutoCompleteSelectMultipleField("keywords", required=False)

    class Meta:
        model = Account
        fields = ["name", "number", "balance", "bank", "account_type", "notes", "keywords"]
