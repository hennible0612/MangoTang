# Generated by Django 4.0 on 2021-12-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_order_order_number_alter_order_total_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller_code',
            field=models.IntegerField(),
        ),
    ]
