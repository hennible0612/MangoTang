# Generated by Django 4.0.1 on 2022-02-07 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_orderitemoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitemoption',
            name='item_option_bool',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
