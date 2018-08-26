# Generated by Django 2.0.7 on 2018-08-18 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_invoice_client'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoices.Invoice'),
        ),
    ]