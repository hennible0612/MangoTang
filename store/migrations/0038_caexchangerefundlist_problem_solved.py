# Generated by Django 3.2.12 on 2022-03-04 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_caexchangerefundlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='caexchangerefundlist',
            name='problem_solved',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
