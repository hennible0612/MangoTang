# Generated by Django 4.0.1 on 2022-02-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='post_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
