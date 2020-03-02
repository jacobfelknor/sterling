from ajax_select.fields import AutoCompleteField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Layout, Row, Submit, HTML
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


class ConfirmTransactionForm(forms.Form):
    def __init__(self, *args, **kwargs):

        fields = kwargs.pop("fields", [("name_0", "amount_0", "category_0", "date_0", "notes_0")],)
        super().__init__(*args, **kwargs)

        form_divs = []

        for field in fields:
            self.fields[field[0]] = forms.CharField(label="Name")
            self.fields[field[1]] = forms.DecimalField(label="Amount", decimal_places=2)
            self.fields[field[2]] = AutoCompleteField("categories", label="Category")
            self.fields[field[3]] = forms.DateTimeField(
                input_formats=["%m/%d/%Y"],
                widget=forms.DateInput(attrs={"autocomplete": "off"}, format="%m/%d/%Y"),
                label="Date",
            )
            self.fields[field[4]] = forms.CharField(label="Notes")
            # print(fields[field[4]])
            form_divs.append(
                Div(
                    Column(field[0], css_class="col-4"),
                    Column(field[1], css_class="col-2"),
                    Column(field[2], css_class="col-2"),
                    Column(field[3], css_class="col-2"),
                    Column(field[4], css_class="col-2"),
                    css_class="row",
                ),
            )
            # if field != fields[-1]:
            #     form_divs.append(HTML("<hr>"))

        self.helper = FormHelper()
        self.helper.layout = Layout(Div(*form_divs), Submit("submit", "Submit"))

