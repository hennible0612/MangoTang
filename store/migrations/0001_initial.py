# Generated by Django 4.0 on 2021-12-29 07:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carosel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('banner_title', models.CharField(blank=True, max_length=200, null=True)),
                ('banner_description', models.CharField(blank=True, max_length=200, null=True)),
                ('href', models.CharField(default='#', max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=200)),
                ('phone_number', models.CharField(max_length=50)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('payment_state', models.BooleanField(default=False)),
                ('shipping_fee', models.IntegerField(blank=True, null=True)),
                ('track_number', models.IntegerField(blank=True, null=True)),
                ('order_number', models.IntegerField(blank=True, null=True)),
                ('total_fee', models.IntegerField(blank=True, null=True)),
                ('recipent_address1', models.CharField(max_length=200)),
                ('recipent_address2', models.CharField(max_length=200)),
                ('recipent_number', models.CharField(max_length=50)),
                ('recipent_name', models.CharField(max_length=50)),
                ('order_request', models.CharField(max_length=100)),
                ('orderer_number', models.CharField(max_length=100)),
                ('orderer_name', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('image_detail', models.ImageField(blank=True, null=True, upload_to='')),
                ('image_title', models.ImageField(blank=True, null=True, upload_to='')),
                ('image_introduce', models.ImageField(blank=True, null=True, upload_to='')),
                ('seller_code', models.IntegerField()),
                ('price_discount', models.IntegerField(null=True)),
                ('discount', models.IntegerField(null=True)),
                ('stock', models.IntegerField()),
                ('first_title', models.CharField(max_length=200)),
                ('second_title', models.CharField(max_length=200)),
                ('shipment_price', models.IntegerField(blank=True)),
                ('hash_tag', models.CharField(max_length=200)),
                ('option_bool', models.BooleanField(default=False, null=True)),
                ('option_total', models.IntegerField(blank=True, null=True)),
                ('collection_tag', models.CharField(max_length=200, null=True)),
                ('item_company', models.CharField(max_length=200)),
                ('product_status', models.BooleanField(default=False, null=True)),
                ('option1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='op1', to='store.product')),
                ('option2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='op2', to='store.product')),
                ('option3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='op3', to='store.product')),
                ('option4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='op4', to='store.product')),
                ('option5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='op5', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rating', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('short_review', models.CharField(blank=True, max_length=50, null=True)),
                ('long_review', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('review_bool', models.BooleanField(default=False, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
    ]
