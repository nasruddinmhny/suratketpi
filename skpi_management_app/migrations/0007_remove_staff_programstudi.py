# Generated by Django 3.2.9 on 2022-03-16 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skpi_management_app', '0006_staff_programstudi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='programstudi',
        ),
    ]
