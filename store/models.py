from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserForm(UserCreationForm):
    name = forms.CharField(label="이름")
    email = forms.EmailField(label="이메일")
    phone_number = forms.CharField(label="전화번호")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "name", "email", "phone_number")


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  # Customer 하나당 User하나
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    allowPromotions = models.BooleanField(default=False, null=True, blank=True)
    post_code = models.CharField(max_length=50, null=True, blank=True)
    recipent_address1 = models.CharField(max_length=200, null=True, blank=True)
    recipent_address2 = models.CharField(max_length=200, null=True, blank=True)
    join_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)  # 제품이름
    price = models.FloatField(null=False, blank=False)
    image_detail = models.ImageField(null=True, blank=True)  # 제품 상세 정보
    image_title = models.ImageField(null=True, blank=True)  # 메인 이미지
    image_introduce = models.ImageField(null=True, blank=True)  # 제품 소개
    seller_code = models.CharField(max_length=50, null=False, blank=False)  # 제품
    price_discount = models.FloatField(null=True)  # 할인된 가격
    discount = models.IntegerField(null=True)  # 할인율
    stock = models.IntegerField()  # 수량
    first_title = models.CharField(max_length=200)  # 제품 상세페이지 메인 타이틀
    second_title = models.CharField(max_length=200)  # 제품 상세페이지 두 번째 타이틀
    shipment_price = models.IntegerField(blank=True)  # 배송 비용용    hash_tag = models.CharField(max_length=200)
    option_bool = models.BooleanField(default=False, blank=False, null=True)  # 옵션의 유무
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
    payment_state = models.BooleanField(default=False)
    shipping_fee = models.IntegerField(null=True, blank=True)  # 배송 비용
    order_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    total_fee = models.IntegerField(null=True, blank=True)  # 총 가격
    post_code = models.CharField(max_length=200, null=True, blank=True)
    recipent_address1 = models.CharField(max_length=200, null=False)
    recipent_address2 = models.CharField(max_length=200, null=False)
    recipent_number = models.CharField(max_length=50, null=False)  # 받는 사람 번호
    recipent_name = models.CharField(max_length=50, null=False)  # 받는 사람 이름
    order_request = models.CharField(max_length=100, null=False)  # 요청 사항
    orderer_number = models.CharField(max_length=100, null=False)  # 주문자 번호
    orderer_name = models.CharField(max_length=100, null=False)  # 주문자 이름

    @property
    def get_all_item_name(self):  # 옵션의 이름 다가져오기
        orderitems = self.orderitem_set.all()  # 해당 order의 자식 가져와서
        data = ""
        for name in orderitems:
            data += name.get_name + ", "
        data = data.strip(', ')
        return data

    @property
    def get_cart_total(self):  # 카트에 있는 총 비용 (옵션 제외)
        orderitems = self.orderitem_set.all()  # 해당 order의 자식 가져와서
        total = sum([item.get_total for item in orderitems])  # 다더함함
        return total

    @property
    def get_cart_items(self):  # 카트에 있는 총 수량 (옵션 제외)
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_option_total(self):  # 카트의 있는 옵션의 총 비용
        orderitems = self.orderitem_set.all()  # 해당 order의 자식 가져와서
        total = sum([item.get_option_cart_total for item in orderitems])  # 다더함함
        return total

    @property
    def get_total(self):  # 카트에 있는 옵션, 제품의 가격
        orderitems = self.orderitem_set.all()  # 해당 order의 자식 가져와서
        total = sum([item.get_total for item in orderitems])  # 다더함함
        optionTotal = sum([item.get_option_cart_total for item in orderitems])  # 다더함함
        return total + optionTotal

    @property
    def get_deliver_price(self):  # 카트에 있는 모든 옵션의 가격
        orderitems = self.orderitem_set.all()
        total = sum([item.get_delivery_price for item in orderitems])
        return total

    @property
    def get_all_price(self):  # 카트에 있는 옵션, 제품, 배송비 포함 가격
        orderitems = self.orderitem_set.all()
        deliverTotal = sum([item.get_delivery_price for item in orderitems])
        itemTotal = sum([item.get_total for item in orderitems])  # 다더함함
        optionTotal = sum([item.get_option_cart_total for item in orderitems])  # 다더함함
        return int(deliverTotal + itemTotal + optionTotal)

    def __str__(self):
        if self.order_number == None:
            return "주문번호: -" + " 상태: " + str(self.order_status)
        else:
            return "주문번호" + str(self.order_number) + "상태" + str(self.order_status) + "받는이: " + str(
                self.recipent_name) + "주문자: " + str(self.orderer_name)


class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_name = models.CharField(max_length=200, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)  # 송장번호
    payment_state = models.BooleanField(default=False)  # 결제 상태
    shipping_fee = models.IntegerField(null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)  # 주문번호
    email = models.EmailField(null=True, blank=True)
    total_fee = models.IntegerField(null=True, blank=True)
    post_code = models.CharField(max_length=200, null=True, blank=True)
    recipent_address1 = models.CharField(max_length=200, null=False)
    recipent_address2 = models.CharField(max_length=200, null=False)
    recipent_number = models.CharField(max_length=50, null=False)
    recipent_name = models.CharField(max_length=50, null=False)
    order_request = models.CharField(max_length=100, null=False)
    orderer_number = models.CharField(max_length=100, null=False)
    orderer_name = models.CharField(max_length=100, null=False)
    receipt_url = models.CharField(max_length=500, null=True, blank=True)  # 아임포트 결제 영수증
    status = models.CharField(max_length=100, null=True, blank=True)  # 주문 상태
    emb_pg_provider = models.CharField(max_length=100, null=True,
                                       blank=True)  # 아임포트 결제 방법 (네이버페이, 카카오 페에, 토스 페이... etc)
    imp_uid = models.CharField(max_length=100, null=True, blank=True)  # 아임포트 주문번호
    pay_method = models.CharField(max_length=100, null=True, blank=True)  # 결제방법 (카드, 무통장... etc)

    @property
    def get_total(self):
        total = self.total_fee + self.shipping_fee
        return total


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    option_name = models.CharField(max_length=200)
    option_seller_code = models.CharField(max_length=50, null=False, blank=False)
    option_price = models.FloatField(null=False, blank=False)
    option_stock = models.IntegerField()
    option_status = models.BooleanField(default=False, blank=False, null=True)

    def __str__(self):
        return " 옵션이름 : " + self.option_name


class OrderItem(models.Model):
    DELIVER_COMPANY = (
        ('04', 'CJ대한통운'),
        ('05', '한진택배'),
        ('08', '롯데택배'),
        ('06', '로젠택배'),
        ('01', '우체국택배'),
        ('46', 'CU편의점택배'),
        ('24', 'GS Postbox 택배	'),
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    orderHistory = models.ForeignKey(OrderHistory, on_delete=models.SET_NULL, null=True)
    deliver_state = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    item_option_bool = models.BooleanField(default=False, blank=False, null=True)
    deliver_company = models.CharField(max_length=200, choices=DELIVER_COMPANY, null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True) # 송장번호

    @property
    def get_all_option_name(self): # orderitemoption의 이름을 가지고 온다.
        orderOptions = self.orderitemoption_set.all()
        data = ""
        for name in orderOptions:
            data += name.get_option_name + ", "
        data = data.strip(', ')
        return data

    @property
    def get_name(self):
        return self.product.product_name

    @property
    def get_option_bool(self):
        return self.item_option_bool

    @property  # 배송비
    def get_delivery_price(self):
        return self.product.shipment_price

    @property  # 제품 가격
    def get_total(self):
        total = self.product.price_discount * self.quantity
        return total

    @property  # 모든 옵션 가격
    def get_option_cart_total(self):
        orderOptions = self.orderitemoption_set.all()
        total = sum([item.get_total for item in orderOptions])
        return total

    @property  # 옵션 포함 가격
    def get_all_total(self):
        total = self.product.price_discount * self.quantity
        orderOptions = self.orderitemoption_set.all()  # 해당 order의 자식 가져와서
        total += sum([item.get_total for item in orderOptions])  # 다더함함
        return total

    def __str__(self):
        return "아이템" + str(self.get_option_cart_total) + "아이템 이름: " + self.product.product_name


class OrderItemOption(models.Model):
    order_item_option = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_option_name(self):
        return self.product_option.option_name

    @property
    def get_total(self):
        total = self.product_option.option_price * self.quantity
        return total

    def __str__(self):
        return "부모 아이템 이름: " + str(
            self.order_item_option.product.product_name) + "옵션 이름: " + self.product_option.option_name + " 옵션 가격: " + str(
            self.get_total)


class ShippingAddress(models.Model): # 구현해야할 부분 여러가지 배송 정보를 저장하고 싶을때 사용
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
    order_number = models.IntegerField(null=True, blank=True)  # 주문번호
    short_review = models.CharField(max_length=50, null=True, blank=True)  # 한줄 리뷰
    long_review = models.CharField(max_length=200, null=True, blank=True)  # 상세 리뷰
    date_added = models.DateTimeField(default=datetime.now)
    image = models.ImageField(null=True, blank=True)
    review_bool = models.BooleanField(default=False, blank=False, null=True)

    review_user_name = models.CharField(default="", blank=True, null=True, max_length=200)
    image_url = models.CharField(default="", blank=True, null=True, max_length=200)

    @property
    def get_user_name(self):
        return self.customer.name

    @property
    def imageURL(self):
        try:
            url_image = self.image.url
        except:
            url_image = ''

        return url_image

    def __str__(self):
        return " 주문자 : " + self.customer.name + " 제품이름: " + self.product.product_name + " 리뷰  : " + self.short_review


class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    question_body = models.CharField(max_length=150, null=True, blank=False)
    question_answer = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(default=datetime.now)
    image = models.ImageField(null=True, blank=True)
    question_state = models.BooleanField(default=False, blank=False)
    question_public = models.BooleanField(default=False, blank=False)

    review_user_name = models.CharField(default="", blank=True, null=True, max_length=200)

    def __str__(self):
        return " 질문 : " + self.question_body + " 질문자 : " + self.customer.name

    def imageURL(self):
        try:
            url_image = self.image.url
        except:
            url_image = ''

        return url_image


class CAExchangeRefundList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    orderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    rqstExrfn = models.CharField(max_length=200, null=True, blank=True)
    reason = models.CharField(max_length=300, null=True, blank=True)
    date_sent = models.DateTimeField(default=datetime.now)
    problem_solved = models.BooleanField(default=False, blank=False, null=True)
