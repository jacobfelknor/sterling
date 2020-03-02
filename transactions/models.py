import uuid

from django.db import models
from django.urls import reverse

from accounts.models import Account

# Create your models here.


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField()
    name = models.CharField("Transaction Name", max_length=200)
    amount = models.DecimalField("Amount", max_digits=65, decimal_places=2, null=True)
    category = models.CharField("Category", max_length=100, null=True)
    date = models.DateField("Date", null=True)
    notes = models.TextField(null=True)

    class Meta:
        unique_together = ("account", "name", "amount", "category", "date")

    def get_absolute_url(self):
        return reverse("transactions:view", args=(self.slug,))

    def save(self, *args, **kwargs):
        self.slug = self.uuid
        # standardize the categories for consitancy
        category_words = self.category.split()
        self.category = ""
        for word in category_words:
            if word != category_words[-1]:
                self.category += word.capitalize() + " "
            else:
                self.category += word.capitalize()
        super(Transaction, self).save(*args, **kwargs)
        # only save account balance after the transaction has been successfully saved
        self.account.balance += self.amount
        self.account.save()


class TempTransaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="temp_transactions")

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField()
    name = models.CharField("Transaction Name", max_length=200)
    amount = models.DecimalField("Amount", max_digits=65, decimal_places=2, null=True)
    category = models.CharField("Category", max_length=100, null=True)
    date = models.DateField("Date", null=True)
    notes = models.TextField(null=True)

    # keep track of what items are done together
    # batch = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # class Meta:
    #     unique_together = ("account", "name", "amount", "category", "date")

    # def get_absolute_url(self):
    #     return reverse("transactions:view", args=(self.slug,))

    def save(self, *args, **kwargs):
        self.slug = self.uuid
        # standardize the categories for consitancy
        category_words = self.category.split()
        self.category = ""
        for word in category_words:
            if word != category_words[-1]:
                self.category += word.capitalize() + " "
            else:
                self.category += word.capitalize()
        super().save(*args, **kwargs)
