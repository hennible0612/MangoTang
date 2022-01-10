# Generated by Django 4.0 on 2022-01-10 08:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_productreview_date_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_body', models.CharField(blank=True, max_length=150, null=True)),
                ('date_added', models.DateField(default=datetime.datetime.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('question_state', models.BooleanField(default=False, null=True)),
                ('question_public', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
