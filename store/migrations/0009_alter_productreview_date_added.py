# Generated by Django 4.0 on 2022-01-20 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_productquestion_question_public_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
