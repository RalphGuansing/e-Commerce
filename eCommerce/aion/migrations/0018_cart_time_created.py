# Generated by Django 2.0.2 on 2018-03-15 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aion', '0017_auto_20180315_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='time_created',
            field=models.TimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
