# Generated by Django 2.2.4 on 2019-09-26 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20190925_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(max_length=100, null=True, verbose_name='Category'),
        ),
    ]
