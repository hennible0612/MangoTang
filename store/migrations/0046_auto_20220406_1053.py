# Generated by Django 3.2.12 on 2022-04-06 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0045_alter_orderitem_deliver_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='recipent_address1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='recipent_address2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
