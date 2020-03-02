# Generated by Django 2.2.8 on 2020-02-08 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200111_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('Checking', 'Checking'), ('Savings', 'Savings'), ('Investment', 'Investment'), ('Credit', 'Credit'), ('Other', 'Other')], max_length=10, verbose_name='Type'),
        ),
    ]
