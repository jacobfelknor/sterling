from django.forms import ModelForm
from .models import Transaction
from django import forms

from ajax_select.fields import AutoCompleteField

class CategoryForm(forms.Form):
    pass


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'amount']
    
    category = AutoCompleteField('categories')
    date = forms.DateTimeField(input_formats=['%m/%d/%Y'], widget=forms.TextInput(attrs={'autocomplete':'off'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off'}))


    # This seems to be broken for now:
    # widgets = {
    #         'date': forms.DateInput(attrs={'class': 'date'}, format='%d/%m/%Y %H:%M'),
    #         'notes': forms.TextInput,
    #     }
