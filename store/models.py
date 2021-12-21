from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    GENDER_CHOICES = (
        ('M','Male'),
        ('M','Female'),
        ('N','Unknown'),
    )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #Customer 하나당 User하나
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=50, null=False)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    mileage = models.IntegerField()
    join_date = models.DateField()
    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    seller_code = models.IntegerField(null=False)
    price_discount = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    stock = models.IntegerField()
    first_title = models.CharField(max_length=200)
    second_title = models.CharField(max_length=200)
    shipment_price = models.IntegerField(blank=True)
    hash_tag = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200, null=True, blank=True)
    option2 = models.CharField(max_length=200, null=True, blank=True)
    option3 = models.CharField(max_length=200, null=True, blank=True)
    option4 = models.CharField(max_length=200, null=True, blank=True)
    option5 = models.CharField(max_length=200, null=True, blank=True)
    collection_tag = models.CharField(max_length=200, null=True)
    item_company = models.CharField(null=False,max_length=200)


    def __str__(self):
        return self.product_name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment_state = models.BooleanField(default=False)
    shipping_fee = models.IntegerField(null=True)
    traking_number = models.IntegerField(null=True, blank=True)
    order_number = models.IntegerField(null=True)
    total_fee = models.IntegerField(null=True)


    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address