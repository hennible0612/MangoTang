# Generated by Django 4.0 on 2022-01-05 09:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_customer_address1_customer_address2_customer_mileage'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='date_added',
            field=models.DateField(default=datetime.datetime(2022, 1, 5, 18, 59, 20, 92586)),
        ),
    ]