# Generated by Django 2.2.4 on 2019-09-06 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190819_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.FloatField(default=0, verbose_name='Balance'),
        ),
    ]
