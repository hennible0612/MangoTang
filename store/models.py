from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms


# class UserForm(UserCreationForm):
#     email = forms.EmailField(label="이메일")
#
#     class Meta:
#         model = User
#         fields = ("username", "password1", "password2", "email")
# # Create your models here.

class Customer(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('M', 'Female'),
        ('N', 'Unknown'),
    )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  # Customer 하나당 User하나

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    mileage = models.IntegerField()
    join_date = models.DateField()
    address1 = models.CharField(max_length=200, null=False)
    address2 = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    image_detail = models.ImageField(null=True, blank=True)
    image_title = models.ImageField(null=True, blank=True)
    image_introduce = models.ImageField(null=True, blank=True)
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
    item_company = models.CharField(null=False, max_length=200)
    product_status = models.BooleanField(default=False, blank=False, null=True)

    @property
    def imageURL(self):
        try:
            url_detail = self.image_detail.url
            url_title = self.image_title.url
            url_introduce = self.image_introduce.url
        except:
            url_detail = ''
            url_title = ''
            url_introduce = ''
        return url_detail, url_title, url_introduce

    def __str__(self):
        return self.product_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    payment_state = models.BooleanField(default=False)
    shipping_fee = models.IntegerField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)
    total_fee = models.IntegerField(null=True, blank=True)

    recipent_address1 = models.CharField(max_length=200, null=False)
    recipent_address2 = models.CharField(max_length=200, null=False)
    recipent_number = models.CharField(max_length=50, null=False)
    recipent_name = models.CharField(max_length=50, null=False)
    order_request = models.CharField(max_length=100, null=False)
    orderer_number = models.CharField(max_length=100, null=False)
    orderer_name = models.CharField(max_length=100, null=False)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()  # 해당 order의 자식 가져와서
        total = sum([item.get_total for item in orderitems])  # 다더함함
        return total


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


    def __str__(self):
        return " 주문자 : " + self.customer.email


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name

    @property
    def get_total(self):
        total = self.product.price_discount * self.quantity
        return total


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
    image = models.ImageField(null=True, blank=True)
    banner_title = models.CharField(max_length=200, null=True, blank=True)
    banner_description = models.CharField(max_length=200, null=True, blank=True)
    href = models.CharField(max_length=200, default='#', null=True, blank=False)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    star_rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True,
                                      null=True)
    short_review = models.CharField(max_length=50, null=True, blank=True)
    long_review = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    review_bool = models.BooleanField(default=False, blank=False, null=True)

    def __str__(self):
        return " 주문자 : " + self.customer.email + " 주소  : " + self.short_review
