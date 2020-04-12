from ajax_select.fields import AutoCompleteField
from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelForm
from crispy_forms.layout import HTML, Button, Column, Div, Layout, Row, Submit

from .models import Transaction

# class TransactionForm(ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ["name", "amount", "category", "date", "notes"]

#     category = AutoCompleteField("categories")
#     date = forms.DateTimeField(
#         input_formats=["%m/%d/%Y"], widget=forms.DateInput(attrs={"autocomplete": "off"}, format="%m/%d/%Y")
#     )
#     notes = forms.CharField(widget=forms.Textarea(attrs={"autocomplete": "off"}))
#     widget = forms.DateInput(
#         attrs={"class": "datepicker form-control", "placeholder": "Select a date"}, format="%m/%d/%Y"
#     )

#     # This seems to be broken for now:
#     # widgets = {
#     #         'date': forms.DateInput(attrs={'class': 'date'}, format='%d/%m/%Y %H:%M'),
#     #         'notes': forms.TextInput,
#     #     }


class TransactionForm(forms.Form):
    """
        Transaction Form. Dynamically generated based on the number of ledge entries
    """

    # Non-variable fields. One instance per form
    date = forms.DateTimeField(
        input_formats=["%m/%d/%Y"], widget=forms.DateInput(attrs={"autocomplete": "off"}, format="%m/%d/%Y")
    )
    name = forms.CharField()
    notes = forms.CharField(widget=forms.Textarea(attrs={"autocomplete": "off", "rows": 3}), required=False)

    account_uuid = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        uuid = kwargs.pop("uuid")
        # gather grouped fields associated with a ledger
        grouped_fields = kwargs.pop("grouped_fields", [("ledger_account_0", "ledger_memo_0", "ledger_amount_0",)],)

        super().__init__(*args, **kwargs)
        self.fields["account_uuid"].initial = uuid
        columns = []
        for group in grouped_fields:
            # generate extra fields in the number specified via extra_fields
            self.fields[group[0]] = AutoCompleteField("accounts", label="Account")
            self.fields[group[1]] = forms.CharField(max_length=25, label="Memo", required=False)
            self.fields[group[2]] = forms.DecimalField(max_digits=65, decimal_places=2, label="Amount")

            # Generate dynamic form layout
            visitor_fields = [
                HTML(f"<div class='ledger_row'> <hr> <div class='row'>"),
                Column(group[0], css_class="form-group col-md-3 mb-0"),  # first_name
                Column(group[1], css_class="form-group col-md-4 mb-0"),  # last_name
                Column(group[2], css_class="form-group col-md-4 mb-0"),  # company_name
                HTML(
                    f"""<button type="button" onclick="rm_row($(this).closest('.ledger_row'));" class="form-group btn btn-sm btn-danger">X</button>"""
                ),
                HTML("</div>  <hr> </div>"),
            ]

            columns.append(Div(*visitor_fields))

        # Finish up generating form, including the dynamic rows above
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-4 mb-0"),
                Column("date", css_class="form-group col-md-4 mb-0"),
                Column("notes", css_class="form-group col-md-4 mb-0"),
            ),
            Div(*columns),
            Div(id="additional_rows"),
            Row(
                Column(
                    Button("add_ledger", "Add Another Ledger", css_class="btn btn-success"),
                    css_class="col text-center",
                )
            ),
            Submit("submit", "Save", css_class="btn btn-dark"),
            "account_uuid",
        )
