# Generated by Django 2.2.4 on 2019-08-19 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(null=True, verbose_name='Amount'),
        ),
    ]