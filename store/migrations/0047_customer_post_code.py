# Generated by Django 3.2.12 on 2022-04-06 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0046_auto_20220406_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='post_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
