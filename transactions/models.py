import decimal
import uuid

from django.db import models
from django.urls import reverse

from accounts.models import Account

# Create your models here.


class Transaction(models.Model):
    # To display a transaction, find it's ledgers and sum the totals of ledgers associated with the parent account
    # This number is the "psuedo-amount" of the transaction from the perspective of that account.
    # Next, display the ledges not associated with the account for display
    # For example, for a transaction  food<--checking, a person buys $10 of food they pay out of checking.
    # Viewing Transaction under Checking, |Food | -15
    # viewing transaction under Food, |Checking| 15
    # So, to view transaction for checking, find ledgers in transaction which are *not* associated with
    # checking, and flip their sign for display. This shows where the money went.

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField()
    name = models.CharField("Transaction Name", max_length=200)
    date = models.DateField("Date", null=True)
    notes = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse("transactions:view", args=(self.slug,))

    # def save(self, *args, **kwargs):
    #     self.slug = self.uuid
    #     # standardize the categories for consitancy
    #     category_words = self.category.split()
    #     self.category = ""
    #     for word in category_words:
    #         if word != category_words[-1]:
    #             self.category += word.capitalize() + " "
    #         else:
    #             self.category += word.capitalize()
    #     super().save(*args, **kwargs)
    #     # only save account balance after the transaction has been successfully saved
    #     self.account.balance += self.amount
    #     self.account.save()


class Ledger(models.Model):
    # each transaction's ledgers must add to 0.
    # TRANSACTION_TYPE_CHOICES = [
    #     ("C", "Credit"),
    #     ("D", "Debit"),
    # ]
    # t_type = models.CharField("Type", max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="ledgers")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="ledgers")

    memo = models.CharField("Memo", max_length=100, null=True)
    amount = models.DecimalField("Amount", max_digits=65, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # only save account balance after the transaction has been successfully saved
        print(type(self.amount))

        self.account.balance += decimal.Decimal(self.amount)
        self.account.save()
