# Generated by Django 4.0.3 on 2022-04-13 04:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('skpi_management_app', '0021_alter_konfirmasidata_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='konfirmasidata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 4, 13, 4, 13, 30, 443052, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='konfirmasidata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
