# Generated by Django 4.0 on 2022-01-22 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_productreview_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='review_user_name',
            field=models.CharField(blank=True, default=True, max_length=200, null=True),
        ),
    ]