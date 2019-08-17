from django.db import models
from django.urls import reverse

from users.models import User

# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    
    ACCOUNT_TYPE_CHOICES = [
        ('Checking', 'Checking'),
        ('Savings', 'Savings'),
        ('Investment', 'Investment'),
        ('Other', 'Other'),
    ]

    name = models.CharField('Account Name', max_length=50)
    number = models.IntegerField('Account Number', unique=True)
    account_type = models.CharField('Type', max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    bank = models.CharField('Bank', max_length=20, null=True)
    notes = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('accounts:view', args=(self.id,)) #pylint: disable=no-member
