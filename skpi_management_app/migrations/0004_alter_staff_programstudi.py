# Generated by Django 3.2.9 on 2022-03-15 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skpi_management_app', '0003_remove_staff_nama'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='programstudi',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='skpi_management_app.programstudi'),
            preserve_default=False,
        ),
    ]
