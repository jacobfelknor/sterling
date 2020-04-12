# Generated by Django 2.2.8 on 2020-04-12 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200111_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='parent',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('Asset', 'Asset'), ('Liability', 'Liability'), ('Expense', 'Expense'), ('Income', 'Income')], max_length=10, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='account',
            name='number',
            field=models.CharField(max_length=50, verbose_name='Account Number'),
        ),
    ]
