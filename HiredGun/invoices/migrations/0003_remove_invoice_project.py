# Generated by Django 2.0.7 on 2018-08-19 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_invoice_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='project',
        ),
    ]