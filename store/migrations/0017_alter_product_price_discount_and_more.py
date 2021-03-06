# Generated by Django 4.0 on 2022-01-26 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_product_option1_remove_product_option2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_discount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller_code',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=200)),
                ('option_seller_code', models.CharField(max_length=50)),
                ('option_price', models.FloatField()),
                ('option_stock', models.IntegerField()),
                ('option_status', models.BooleanField(default=False, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
