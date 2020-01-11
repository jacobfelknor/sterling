import uuid

from django.db import models
from django.urls import reverse

from users.models import User

# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

    ACCOUNT_TYPE_CHOICES = [
        ("Checking", "Checking"),
        ("Savings", "Savings"),
        ("Investment", "Investment"),
        ("Other", "Other"),
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField()
    name = models.CharField("Account Name", max_length=50)
    number = models.IntegerField("Account Number")
    balance = models.DecimalField("Balance", max_digits=1000, decimal_places=2, default=0)
    account_type = models.CharField("Type", max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    bank = models.CharField("Bank", max_length=20, null=True)
    notes = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse("accounts:view", args=(self.slug,))

    def save(self, *args, **kwargs):
        self.slug = self.uuid
        super(Account, self).save(*args, **kwargs)
