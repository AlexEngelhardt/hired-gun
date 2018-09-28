# Generated by Django 2.0.7 on 2018-09-28 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20180902_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='private_note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='units_worked',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4),
        ),
    ]
