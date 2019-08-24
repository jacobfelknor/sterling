from django.forms import ModelForm
from .models import Transaction
from django import forms

from .widgets import FengyuanChenDatePickerInput

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'amount', 'category', 'date', 'notes']

    widgets = {
            'date': forms.DateInput(attrs={'class': 'date'}, format='%d/%m/%Y %H:%M')
        }
