# Generated by Django 2.0.2 on 2018-03-10 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aion', '0008_auto_20180310_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address_details',
            name='address_type',
        ),
        migrations.RemoveField(
            model_name='address_details',
            name='user_id',
        ),
        migrations.AddField(
            model_name='user_details',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='aion.Address_Details'),
        ),
        migrations.AddField(
            model_name='user_details',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='aion.Address_Details'),
        ),
    ]
