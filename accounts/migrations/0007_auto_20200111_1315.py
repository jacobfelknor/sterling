# Generated by Django 2.2.4 on 2020-01-11 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_account_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=65, verbose_name="Balance"),
        ),
    ]
