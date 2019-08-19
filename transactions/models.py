import uuid

from django.db import models
from django.urls import reverse

from accounts.models import Account

# Create your models here.


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField()
    name = models.CharField('Transaction Name', max_length=50)
    amount = models.FloatField('Amount', null=True)
    category = models.CharField('Category', max_length=20, null=True)
    date = models.DateField('Date', null=True)
    notes = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('transactions:view', args=(self.slug,)) #pylint: disable=no-member

    def save(self, *args, **kwargs):
        self.slug = self.uuid
        super(Transaction, self).save(*args, **kwargs)
