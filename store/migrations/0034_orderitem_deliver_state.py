# Generated by Django 3.2.12 on 2022-03-03 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_rename_order_state_orderhistory_deliver_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='deliver_state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]