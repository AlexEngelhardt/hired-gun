# Generated by Django 2.0.7 on 2018-08-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]