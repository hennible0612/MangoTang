import json
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime

from django.urls import reverse

from MangoTang import settings
from .models import *

# Create your views here.
"""
스토어 메인화면
"""


def store(request):
    if request.user.is_authenticated:  # 로그인 유저일시
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)
        items = order.orderitem_set.all()  # orderitem은 Order의 자식 그래서 쿼리 가능
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()  # product 정보 다가져옴
    carousel = Carosel.objects.all()  # 캐러솔 가져옴
    carousel_length = len(carousel)

    context = {'products': products, 'carousel': carousel, 'carousel_length': carousel_length, 'cartItems': cartItems}

    return render(request, 'store/store.html', context)


"""
제품 설명
메인화면에서 클릭시 이동할 제품 페이지
"""


def productDetail(request, seller_code):
    product = Product.objects.get(seller_code=seller_code)

    review_page = request.GET.get('page', 1)  # 리뷰 페이지
    question_page = request.GET.get('page', 1)  # 리뷰 페이지

    reviews = product.productreview_set.all().order_by('-date_added')
    questions = product.productquestion_set.all().order_by('-date_added')

    # 리뷰 페이징
    review_paginator = Paginator(reviews, 5)
    review_obj = review_paginator.get_page(review_page)

    # 제품 질문 페이징
    question_paginator = Paginator(questions, 5)
    question_obj = question_paginator.get_page(question_page)

    if (product.option_bool == True):
        options = product.productoption_set.all()
    else:
        options = None

    context = {'product': product, 'review_page': review_page, 'review_obj': review_obj
        , 'question_page': question_page, 'questions': questions, 'total_review': len(reviews)
        , 'total_question': len(questions), 'question_obj': question_obj, 'reviews': reviews, 'options': options}
    return render(request, 'store/productdetail.html', context)


"""
내 카트
"""


@login_required(login_url='/login')
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    items = order.orderitem_set.all()  # orderitem은 Order의 자식 그래서 쿼리 가능
    cartItems = order.get_cart_items
    itemOption = []
    # for item in items: #해당 아이템 불리언이 true이면
    #     if (item.get_option_bool == True):
    #         print(item , "option is true")
    #     else:
    #         print(item , "option is False")

    if (bool(items) == True):  # 카트 비어있는지 확인
        for item in items:
            itemOption += OrderItemOption.objects.filter(order_item_option=item)
    else:
        items = []
        itemOption = []

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'itemOption': itemOption}

    return render(request, 'store/cart.html', context)


"""
로그인 요청 처리
"""


def user_login(request):
    context = {}
    return render(request, 'store/login.html', context)


"""
회원가입 요청 처리
"""


def register(request):
    if request.method == "POST":

        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            phone_number = form.cleaned_data.get('phone_number')
            address1 = form.cleaned_data.get('address1')
            address2 = form.cleaned_data.get('address2')
            user = User.objects.get(username=username)

            Customer.objects.create(user=user, name=name, email=email, phone_number=phone_number, address1=address1,
                                    address2=address2)
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('store')
    else:
        form = UserForm()

    return render(request, 'store/register.html', {'form': form})


"""
결제 화면
"""


@login_required(login_url='/login')
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    items = order.orderitem_set.all()  # orderitem은 Order의 자식 그래서 쿼리 가능
    cartItems = order.get_cart_items
    itemOption = []
    if (bool(items) == True):
        for item in items:
            itemOption += OrderItemOption.objects.filter(order_item_option=item)

        context = {'items': items, 'order': order, 'cartItems': cartItems, 'itemOption': itemOption}
        return render(request, 'store/checkout.html', context)

    else:

        return render(request, 'permisson.html')


"""
장바구니에 물품 추가 JSON 응답
"""


def updateItem(request):
    if request.user.is_authenticated:  # 로그인 유저일시

        data = json.loads(request.body)  # JSON body data에저장
        option = data["option"]
        if (option == 'false'):
            seller_code = data['sellerCode']  # 각각 body에 있는 필요한 값저장
            action = data['action']
            quantity = data['quantity']
            customer = request.user.customer  # 현재 customer
            product = Product.objects.get(seller_code=seller_code)  # 해당하는 productId가져옴
            order, created = Order.objects.get_or_create(customer=customer,
                                                         order_status=False)  # 주문객체  만들거나 가져옴 상태 False
            orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                                 product=product)  # 해당 orderd와 해당 product를 가지고 있는 orderitem 생성
            if action == 'add':
                orderItem.quantity = (orderItem.quantity + 1)
            elif action == 'remove':
                orderItem.quantity = (orderItem.quantity - 1)
            elif action == 'set':
                orderItem.quantity = quantity

            orderItem.save()  # DB에 저장

            if int(orderItem.quantity) <= 0:
                orderItem.delete()

            return JsonResponse('Item was added', safe=False)
        else:
            seller_code = data['itemSellercode']  # 옵션의 부모 제품 코드
            productQuantity = data['productQuantity']  # 옵션의 부모 개수
            customer = request.user.customer  # 현재 customer
            product = Product.objects.get(seller_code=seller_code)  # 해당하는 productId가져옴
            order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 현재 고객 주문
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderItem.item_option_bool = True  # 이 orderitem의 옵션은 True이다.
            orderItem.quantity = productQuantity
            orderItem.save()

            for x, y in zip(data['options'], data['quantity']):
                sellerCode = data['options'][x]
                options = ProductOption.objects.get(option_seller_code=str(sellerCode))  # 해당 sellercode의 옵션 가져오고
                orderItemOption, created = OrderItemOption.objects.get_or_create(order_item_option=orderItem,
                                                                                 product_option=options)
                orderItemOption.quantity = data['quantity'][y]
                orderItemOption.save()
            return JsonResponse('Item was added', safe=False)
    else:
        return JsonResponse('false', safe=False)


"""
카트에서 업데이트 아이템

"""


def updateCartItem(request):
    data = json.loads(request.body)  # JSON body data에저장
    option = data['option']
    if (option == False):
        print("option == False")
        seller_code = data['sellerCode']  # 각각 body에 있는 필요한 값저장
        action = data['action']
        # quantity = data['quantity']

        customer = request.user.customer  # 현재 customer
        product = Product.objects.get(seller_code=seller_code)  # 해당하는 productId가져옴
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 주문객체  만들거나 가져옴 상태 False

        orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                             product=product)  # 해당 orderd와 해당 product를 가지고 있는 orderitem 생성
        if orderItem.quantity == 1 and action == 'remove':
            pass
        elif action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()  # DB에 저장

        data = {
            "itemQuantity": orderItem.quantity,
            "itemDiscountPrice": orderItem.product.price_discount,
            "itemPriceTotal": orderItem.get_total,
            "orderItemTotal": order.get_cart_items,
            "orderItemPriceTotal": order.get_cart_total,
            "cartTotal": order.get_total,

        }
        json_obj = json.dumps(data)

        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        print("option == True")

        seller_code = data['sellerCode']  # 각각 body에 있는 필요한 값저장
        action = data['action']
        code = data['code']  # 부모 코드

        customer = request.user.customer  # 현재 customer
        product = Product.objects.get(seller_code=code)  # 해당하는 productId가져옴
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 현재 고객 주문

        orderItem = OrderItem.objects.get(order=order, product=product)

        options = ProductOption.objects.get(option_seller_code=seller_code)
        orderItemOption = OrderItemOption.objects.get(order_item_option=orderItem, product_option=options)
        if orderItemOption.quantity == 1 and action == 'remove':
            pass
        elif action == 'add':
            orderItemOption.quantity = orderItemOption.quantity + 1
        elif action == 'remove':
            orderItemOption.quantity = orderItemOption.quantity - 1
        orderItemOption.save()
        data = {
            "itemOptionQuantity": orderItemOption.quantity,
            "itemOptionPrice": orderItemOption.product_option.option_price,
            "orderItemPriceTotal": order.get_cart_total,
            "cartTotal": order.get_total,

        }
        json_obj = json.dumps(data)
        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


"""
카트에서 아이템 삭제
"""


def deleteCartItem(request, seller_code):
    data = json.loads(request.body)  # JSON body data에저장
    option = data['option']
    if (option == False):
        customer = request.user.customer  # 현재 customer
        product = Product.objects.get(seller_code=seller_code)  # 해당하는 productId가져옴
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 주문객체  만들거나 가져옴 상태 False
        orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                             product=product)
        orderItem.delete()

        data = {
            "orderItemTotal": order.get_cart_items,
            "orderItemPriceTotal": order.get_cart_total
        }
        json_obj = json.dumps(data)

        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        # 각각 body에 있는 필요한 값저장
        customer = request.user.customer  # 현재 customer
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 현재 고객 주문
        product = Product.objects.get(seller_code=seller_code)
        orderItem = OrderItem.objects.get(order=order, product=product)
        option_code = data['optionCode']

        options = ProductOption.objects.get(option_seller_code=option_code)
        orderItemOption = OrderItemOption.objects.get(order_item_option=orderItem, product_option=options)
        orderItemOption.delete()
        data = {
            "orderItemPriceTotal": order.get_total
        }
        itemOption = orderItem.orderitemoption_set.all()  # 아이템 있는지 테스트용
        if (bool(itemOption) == True):

            pass
        else:
            orderItem.item_option_bool = False
            orderItem.save()

        json_obj = json.dumps(data)

        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


"""
제품 리뷰 가져오는 API
"""


def getReview(request, seller_code, page):
    product = Product.objects.get(seller_code=seller_code)

    review_page = request.GET.get('page', page)  # 리뷰 페이지
    reviews = product.productreview_set.all().order_by('-date_added')  # 여기에 모든 리뷰 들어있음

    review_paginator = Paginator(reviews, 5)
    review_obj = review_paginator.get_page(review_page)

    for review in review_obj:
        review.review_user_name = review.customer.name  # 해당 id의 user이름을 가지고 와서 DB에 저장
        review.image_url = review.imageURL  # 해당 리뷰의 imageURL을 가져와서 DB에 저장

    json_obj = serializers.serialize('json', review_obj)  # 페이징된값

    return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


"""
제품 질문 가져오는 API
"""


def getQuestion(request, seller_code, page):
    current_user = json.loads(request.body)  # 현재 유저 받아옴
    product = Product.objects.get(seller_code=seller_code)

    question_page = request.GET.get('page', page)  # 리뷰 페이지
    questions = product.productquestion_set.all().order_by('-date_added')  # 여기에 모든 리뷰 들어있음

    question_pageinator = Paginator(questions, 5)
    question_obj = question_pageinator.get_page(question_page)

    for question in question_obj:
        question.review_user_name = question.customer.name  # 해당 id의 user이름을 가지고 와서 객체에 저장
        if (question.question_public == False and current_user != question.customer.name):
            question.question_body = "비공개 질문"

    json_obj = serializers.serialize('json', question_obj)  # 페이징된값

    return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


def checkoutPayment(request):
    data = json.loads(request.body)
    customer = request.user.customer  # 현재 customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    if (order.order_status == False):

        order_id = str(customer.id) + str(datetime.now().timestamp())
        order_id = int(float(order_id))

        name = order.get_all_item_name
        order.total_fee = order.get_total
        order.order_number = order_id
        order.shipping_fee = order.get_deliver_price
        order.post_code = data['data']['post_code']
        order.recipent_address1 = data['data']['recipent_address1']
        order.recipent_address2 = data['data']['recipent_address2']
        order.recipent_number = data['data']['recipent_number']
        order.orderer_number = data['data']['orderer_number']
        order.order_request = data['data']['order_request']
        order.recipent_name = data['data']['recipent_name']
        order.orderer_name = data['data']['orderer_name']
        order.email = data['data']['email']
        order.save()

        iamport_data = {
            "merchant_uid": order_id,
            "name": name,
            "amount": order.get_total + order.get_deliver_price,
            "buyer_email": data['data']['email'],
            "buyer_name": data['data']['orderer_name'],
            "buyer_tel": data['data']['orderer_number'],
            "buyer_addr": data['data']['recipent_address1'],
            "post_code": data['data']['post_code'],

        }
        json_obj = json.dumps(iamport_data)

        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:

        return render(request, 'permisson.html')


"""
아임포트 토큰 가져오기
"""


def getToken():
    url = 'https://api.iamport.kr/users/getToken'

    data = {
        'imp_key': settings.imp_key,
        'imp_secret': settings.imp_secret
    }
    req = requests.post(url, data=data)
    access_res = req.json()

    if access_res['code'] == 0:
        return access_res['response']['access_token']
    else:
        return None


"""
아임포트 결제 정보 확인
"""


def getPaymentData(access_res, imp_uid):
    url = 'https://api.iamport.kr/payments/' + imp_uid
    headers = {
        "Authorization": access_res
    }
    req = requests.get(url, headers=headers)
    access_res = req.json()

    if access_res['code'] == 0:
        return access_res
    else:
        return None


def checkoutComplete(request):
    data = json.loads(request.body)
    imp_uid = data['imp_uid']
    merchant_uid = data['merchant_uid']

    access_res = getToken()  # 토큰 가져오기
    iamportData = getPaymentData(access_res, imp_uid)  # 아임포트 서버에서 결제 확인

    # 아임포트 서버랑 우리 몰 서버 결제 금액 비교

    IamportAmount = iamportData["response"]["amount"]  # Iamport 서버 결제 금액
    status = iamportData["response"]["status"]  # 주문 상태

    customer = request.user.customer  # 현재 customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    localAmount = order.get_total + order.get_deliver_price  # 로컬 서버의 결제 금액

    orderhistory = OrderHistory.objects.create(customer=customer)

    if (IamportAmount == localAmount):
        order.order_status = True
        order.payment_state = True
        orderhistory.orderer_name = order.get_all_item_name
        orderhistory.date_ordered = order.date_ordered
        orderhistory.date_completed = datetime.now()
        orderhistory.payment_state = order.payment_state

        orderhistory.shipping_fee = order.shipping_fee
        orderhistory.order_number = order.order_number
        orderhistory.email = order.email
        orderhistory.total_fee = order.total_fee
        orderhistory.post_code = order.post_code
        orderhistory.recipent_address1 = order.recipent_address1
        orderhistory.recipent_address2 = order.recipent_address2
        orderhistory.recipent_number = order.recipent_number
        orderhistory.recipent_name = order.recipent_name
        orderhistory.order_request = order.order_request
        orderhistory.orderer_number = order.orderer_number
        orderhistory.orderer_name = order.orderer_name

        orderhistory.receipt_url = iamportData["response"]["receipt_url"]
        orderhistory.status = iamportData["response"]["status"]
        orderhistory.emb_pg_provider = iamportData["response"]["emb_pg_provider"]
        orderhistory.imp_uid = iamportData["response"]["imp_uid"]
        orderhistory.pay_method = iamportData["response"]["pay_method"]
        order.delete()
        orderhistory.save()
        # order.save()
        json_obj = json.dumps(iamportData)
        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:  # 위조시
        iamportData["response"]["status"] = "forgery"
        json_obj = json.dumps(iamportData)

        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


"""
결제 완료 요약
"""


def checkoutSummery(request, orderId):
    if request.user.is_authenticated:  # 로그인 유저일시
        customer = request.user.customer
        order = OrderHistory.objects.filter(customer=customer, order_number=orderId)

        if order.exists():
            orderhistory = OrderHistory.objects.get(customer=customer, order_number=orderId)

            context = {'orderhistory': orderhistory}
            print(context)
            return render(request, 'store/checkoutsummery.html', context)
        else:
            return render(request, 'permisson.html')

    else:
        return render(request, 'permisson.html')


"""
결제 성공
"""


def paymentSuccess(request):
    print("결제 성공")

    json_obj = {}
    return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


"""
내페이지
"""


@login_required(login_url='/login')
def mypage(request):
    context = {}
    return render(request, 'store/mypage.html', context)


@login_required(login_url='/login')
def customerservice(request):
    context = {}
    return render(request, 'store/customerservice.html', context)


def faq(request):
    context = {}
    return render(request, 'customerservice/faq.html', context)


@login_required(login_url='/login')
def onetoone(request):
    context = {}
    return render(request, 'customerservice/onetoonequestion.html', context)


def notice(request):
    context = {}
    return render(request, 'customerservice/notice.html', context)


# 주문 관리 view
@login_required(login_url='/login')
def orderhistory(request):
    customer = request.user.customer
    orderHistory = OrderHistory.objects.filter(customer=customer)

    context = {'orderHistory': orderHistory}

    return render(request, 'mypage/orderhistory.html', context)


@login_required(login_url='/login')
def ordercancel(request):
    context = {}
    return render(request, 'mypage/ordercancel.html', context)


@login_required(login_url='/login')
def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html', context)


# 마이페이지
@login_required(login_url='/login')
def favoritelist(request):
    context = {}
    return render(request, 'mypage/favoritelist.html', context)


@login_required(login_url='/login')
def couponlist(request):
    context = {}
    return render(request, 'mypage/couponlist.html', context)


@login_required(login_url='/login')
def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html', context)


@login_required(login_url='/login')
def pointlist(request):
    context = {}
    return render(request, 'mypage/pointlist.html', context)


@login_required(login_url='/login')
def qnalist(request):
    context = {}
    return render(request, 'mypage/qnalist.html', context)


@login_required(login_url='/login')
def refundlist(request):
    context = {}
    return render(request, 'mypage/refundlist.html', context)


@login_required(login_url='/login')
def reviewlist(request):
    context = {}
    return render(request, 'mypage/reviewlist.html', context)


@login_required(login_url='/login')
def userinfo(request):
    context = {}
    return render(request, 'mypage/userinfo.html', context)


@login_required(login_url='/login')
def orderdetail(request):
    context = {}
    return render(request, 'mypage/orderdetail.html', context)
