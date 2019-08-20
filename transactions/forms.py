from django.forms import ModelForm
from .models import Transaction
from django import forms

from .widgets import FengyuanChenDatePickerInput

class DateForm(forms.Form):
    date = forms.DateField(
        input_formats=['%d/%m/%Y %H:%M'], 
        widget=FengyuanChenDatePickerInput()
    )


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'amount', 'category', 'date', 'notes']

