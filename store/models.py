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
    image_detail = models.ImageField(null=True,blank=True)
    image_title = models.ImageField(null=True,blank=True)
    image_introduce = models.ImageField(null=True,blank=True)
    seller_code = models.IntegerField(null=False)
    price_discount = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    stock = models.IntegerField()
    first_title = models.CharField(max_length=200)
    second_title = models.CharField(max_length=200)
    shipment_price = models.IntegerField(blank=True)
    hash_tag = models.CharField(max_length=200)
    option_bool = models.BooleanField(default=False, blank=False, null=True)
    option_total = models.IntegerField(blank=True, null=True)
    option1 = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="op1")
    option2 = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="op2")
    option3 = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="op3")
    option4 = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="op4")
    option5 = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="op5")
    collection_tag = models.CharField(max_length=200, null=True)
    item_company = models.CharField(null=False,max_length=200)
    product_status = models.BooleanField(default=False, blank=False, null=True)


    def __str__(self):
        return self.product_name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment_state = models.BooleanField(default=False)
    shipping_fee = models.IntegerField(null=True)
    track_number = models.IntegerField(null=True, blank=True)
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

class Carosel(models.Model):
    image = models.ImageField(null=True,blank=True)
    banner_title = models.CharField(max_length=200, null=True, blank=True)
    banner_description = models.CharField(max_length=200, null=True, blank=True)
    href = models.CharField(max_length=200,default='#', null=True, blank=False)
