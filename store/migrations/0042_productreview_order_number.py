# Generated by Django 3.2.12 on 2022-03-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_customer_allowpromotions'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='order_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
