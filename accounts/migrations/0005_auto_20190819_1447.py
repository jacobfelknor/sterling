# Generated by Django 2.2.4 on 2019-08-19 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190819_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='number',
            field=models.IntegerField(verbose_name='Account Number'),
        ),
    ]
