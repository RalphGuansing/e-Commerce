# Generated by Django 2.0.2 on 2018-03-15 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aion', '0019_auto_20180316_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=2),
        ),
    ]
