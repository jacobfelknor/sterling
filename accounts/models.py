import uuid

from django.db import models
from django.urls import reverse

from users.models import User

# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

    ACCOUNT_TYPE_CHOICES = [
        ("Asset", "Asset"),
        ("Liability", "Liability"),
        ("Expense", "Expense"),
        ("Income", "Income"),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField()
    name = models.CharField("Account Name", max_length=50)
    number = models.CharField("Account Number", max_length=50)
    balance = models.DecimalField("Balance", max_digits=65, decimal_places=2, default=0)
    account_type = models.CharField("Type", max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    bank = models.CharField("Bank", max_length=20, null=True)
    notes = models.TextField(null=True)

    # self recursive relationship (essentially sub-account/categories)
    parent = models.OneToOneField("accounts.Account", on_delete=models.CASCADE, null=True)
    child = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, related_name="children", null=True)

    def get_absolute_url(self):
        return reverse("accounts:view", args=(self.slug,))

    def save(self, *args, **kwargs):
        self.slug = self.uuid
        super(Account, self).save(*args, **kwargs)
