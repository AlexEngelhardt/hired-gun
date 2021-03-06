# Generated by Django 2.0.7 on 2018-09-02 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20180826_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-start_date']},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='session',
            name='units_worked',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4),
        ),
    ]
