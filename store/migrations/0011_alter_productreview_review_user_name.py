# Generated by Django 4.0 on 2022-01-22 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_productreview_review_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='review_user_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
