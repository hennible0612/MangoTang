# Generated by Django 4.0.1 on 2022-02-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_remove_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]