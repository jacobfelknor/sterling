from ajax_select.fields import AutoCompleteField
from django import forms
from django.forms import ModelForm

from .models import Transaction, Category


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

    # def full_clean(self):
    #     try:
    #         _mutable = self.data._mutable
    #         self.data._mutable = True
    #         pre_category = Category.objects.filter(name=self.data["category"])
    #         if len(pre_category) == 0:
    #             # standardize the categories for consitancy
    #             category_words = self.data["category"].split()
    #             name = ""
    #             for word in category_words:
    #                 if word != category_words[-1]:
    #                     name += word.capitalize() + " "
    #                 else:
    #                     name += word.capitalize()
    #             new_category = Category.objects.create(name=name)
    #             self.data["category"] = new_category
    #         else:
    #             self.data["category"] = pre_category.first()
    #         self.data._mutable = _mutable
    #     except AttributeError:
    #         pass
    #     print(type(self.data["category"]))
    #     super().full_clean()

    def clean(self):
        # standardize the categories for consitancy
        category_words = self.cleaned_data["category"].split()
        name = ""
        for word in category_words:
            if word != category_words[-1]:
                name += word.capitalize() + " "
            else:
                name += word.capitalize()
        pre_category = Category.objects.filter(name=name)
        if len(pre_category) == 0:
            new_category = Category.objects.create(name=name)
            self.cleaned_data["category"] = new_category
        else:
            self.cleaned_data["category"] = pre_category.first()
        # self.instance.category = Category.objects.get(id=self.instance.category)
        # print(self.cleaned_data)
        return super().clean()

    # def is_valid(self):
    #     # data = self.data
    # pre_category = Category.objects.filter(name=data["category"])
    # if not pre_category:
    #     print("here")
    #     return False
    #     return super().is_valid()


# class CategoryForm(ModelForm):

# # standardize the categories for consitancy
#     category_words = self.name.split()
#     self.name = ""
#     for word in category_words:
#         if word != category_words[-1]:
#             self.name += word.capitalize() + " "
#         else:
#             self.name += word.capitalize()
