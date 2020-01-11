from ajax_select.fields import AutoCompleteField
from django import forms
from django.forms import ModelForm

from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["name", "amount", "category", "date", "notes"]

    category = AutoCompleteField("categories")
    date = forms.DateTimeField(
        input_formats=["%m/%d/%Y"], widget=forms.DateInput(attrs={"autocomplete": "off"}, format="%m/%d/%Y")
    )
    notes = forms.CharField(widget=forms.Textarea(attrs={"autocomplete": "off"}))
    widget = forms.DateInput(
        attrs={"class": "datepicker form-control", "placeholder": "Select a date"}, format="%m/%d/%Y"
    )

    # This seems to be broken for now:
    # widgets = {
    #         'date': forms.DateInput(attrs={'class': 'date'}, format='%d/%m/%Y %H:%M'),
    #         'notes': forms.TextInput,
    #     }
