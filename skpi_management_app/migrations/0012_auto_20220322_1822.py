# Generated by Django 3.2.9 on 2022-03-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skpi_management_app', '0011_alter_mahasiswa_tempatlahir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mahasiswa',
            name='address',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='mahasiswa',
            name='tempatlahir',
            field=models.CharField(blank=True, max_length=200, verbose_name='Tem. Lahir'),
        ),
    ]
