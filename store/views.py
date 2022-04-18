from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from MangoTang import settings
from .models import *
import json
import requests
import logging
import datetime

logger = logging.getLogger(__name__)

"""
메인페이지
"""


def store(request):
    kw = request.GET.get('kw', '')
    products = Product.objects.all()
    carousel = Carosel.objects.all()
    carousel_length = len(carousel)
    if request.user.is_authenticated:  # 로그인 유저일시
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, order_status=False)
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:  # 소셜로그인 아이디가 customer가 없을경우
            user = request.user
            social = SocialAccount.objects.get(user=user)
            if (social.provider == "naver"):
                customer = Customer.objects.create(user=user, name=social.extra_data['name'],
                                                   email=social.extra_data['email'],
                                                   phone_number=social.extra_data['mobile'], join_date=datetime.now())
            elif (social.provider == "kakao"):
                customer = Customer.objects.create(user=user,
                                                   name=social.extra_data["kakao_account"]["profile"]["nickname"],
                                                   email=social.extra_data["kakao_account"]["email"],
                                                   phone_number="0000", join_date=datetime.now())
            elif (social.provider == "google"):
                customer = Customer.objects.create(user=user, name=social.extra_data["name"],
                                                   email=social.extra_data["email"],
                                                   phone_number="none", join_date=datetime.now())
            else:
                logger.critical("exception error: " + 'view store 소셜 로그인 과정중에 에러')
                return render(request, 'error.html')
            customer.save()
            order, created = Order.objects.get_or_create(customer=customer, order_status=False)
            cartItems = order.get_cart_items
        except Exception as e:
            logger.critical("exception error: " + str(e) + 'view store 소셜 로그인 과정중에 에러')
            return render(request, 'error.html')
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    if kw:  # 검색 키워드가 있을 경우
        products = Product.objects.filter(product_name__contains=kw)
        context = {'products': products, 'carousel': carousel, 'carousel_length': carousel_length,
                   'cartItems': cartItems}
        return render(request, 'store/store.html', context)

    products = products.order_by("?")
    context = {'products': products, 'carousel': carousel, 'carousel_length': carousel_length, 'cartItems': cartItems}

    return render(request, 'store/store.html', context)


"""
제품 설명
메인화면에서 클릭한 제품을
요청하는 페이지
"""


def productDetail(request, seller_code):
    # 쿼리는 제품 고유의 seller_code 사용
    product = Product.objects.get(seller_code=seller_code)

    review_page = request.GET.get('page', 1)  # 리뷰 페이지
    question_page = request.GET.get('page', 1)  # 리뷰 페이지
    # 날짜순 정렬
    reviews = product.productreview_set.all().order_by('-date_added')
    questions = product.productquestion_set.all().order_by('-date_added')
    # 리뷰 페이징
    review_paginator = Paginator(reviews, 5)
    review_obj = review_paginator.get_page(review_page)
    # 제품 질문 페이징
    question_paginator = Paginator(questions, 5)
    question_obj = question_paginator.get_page(question_page)

    # 옵션이 있을 경우 해당 제품의 옵션 쿼리
    if (product.option_bool == True):
        options = product.productoption_set.all()
    else:
        options = None

    context = {'product': product, 'review_page': review_page, 'review_obj': review_obj
        , 'question_page': question_page, 'total_review': len(reviews)
        , 'total_question': len(questions), 'question_obj': question_obj, 'options': options}
    return render(request, 'store/productdetail.html', context)


"""
내 카트
현재 customer의 아이템들과 그 옵션들을 쿼리
쇼핑몰의 카트
"""


@login_required(login_url='account_login')
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    itemOption = []

    # 카트 비어있는지 확인 없을시 빈 객체 return
    if (bool(items) == True):
        for item in items:
            itemOption += OrderItemOption.objects.filter(order_item_option=item)
    else:
        items = []
        itemOption = []

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'itemOption': itemOption}

    return render(request, 'store/cart.html', context)


"""
로그인 페이지 요청 처리
"""


def user_login(request):
    return render(request, 'store/login.html')


"""
회원가입
쇼핑몰 자체 회원가입
"""


def register(request):
    # 비회원 회원가입시
    if request.method == "POST":

        try:

            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                name = form.cleaned_data.get('name')
                phone_number = form.cleaned_data.get('phone_number')
                allowPromotions = form.data.get('allowPromotions')
                user = User.objects.get(username=username)

                Customer.objects.create(user=user, name=name, email=email, phone_number=phone_number,
                                        allowPromotions=allowPromotions)
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('store')
        except Exception as e:
            logger.critical("exception error: " + str(e) + '쇼핑몰 회원가입중 에러')
    else:
        # GET 요청시
        form = UserForm()
    return render(request, 'store/register.html', {'form': form})


"""
장바구니에 물품 추가
"""


def updateItem(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)  # 카트에 추가하는 아이템 정보
        option = data["option"]
        if (option == 'false'):  # 메인 제품만 있을 경우
            seller_code = data['sellerCode']
            action = data['action']
            quantity = data['quantity']
            customer = request.user.customer
            product = Product.objects.get(seller_code=seller_code)

            order, created = Order.objects.get_or_create(customer=customer,
                                                         order_status=False)  # 주문객체  만들거나 가져옴 상태 False
            orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                                 product=product)  # 해당 order와 해당 product를 가지고 있는 orderitem 생성

            #  받은 action에 따라 기능 수행
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
        else:  # 메인제품 + 옵션이 있을 경우
            seller_code = data['itemSellercode']  # 옵션의 부모 제품 코드
            productQuantity = data['productQuantity']  # 옵션의 부모 개수
            customer = request.user.customer
            product = Product.objects.get(seller_code=seller_code)  # 해당하는 productId가져옴
            order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 현재 고객 주문
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderItem.item_option_bool = True  # 해당 아이템 옵션 유뮤 True로 변경
            orderItem.quantity = productQuantity
            orderItem.save()

            # 메인제품의 옵션 추가
            for x, y in zip(data['options'], data['quantity']):
                sellerCode = data['options'][x]
                options = ProductOption.objects.get(option_seller_code=str(sellerCode))
                orderItemOption, created = OrderItemOption.objects.get_or_create(order_item_option=orderItem,
                                                                                 product_option=options)
                orderItemOption.quantity = data['quantity'][y]
                orderItemOption.save()
            return JsonResponse('Item was added', safe=False)
    else:
        return JsonResponse('false', safe=False)


"""
카트에서 메인제품과 메인제품의 옵션들
 add, sub, delete
"""


def updateCartItem(request):
    data = json.loads(request.body)
    option = data['option']
    if (option == False):  # 옵션이 없을 경우
        seller_code = data['sellerCode']
        action = data['action']

        customer = request.user.customer
        product = Product.objects.get(seller_code=seller_code)
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if orderItem.quantity == 1 and action == 'remove':  # 화살표로 제품 삭제 방지
            pass
        elif action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        # 카트의 수량 제품비 합을 change 하기 위해 필요 정보 전달
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
        seller_code = data['sellerCode']  # 각각 body에 있는 필요한 값저장
        action = data['action']
        code = data['code']  # 부모 코드

        customer = request.user.customer  # 현재 customer
        product = Product.objects.get(seller_code=code)  # 해당하는 productId 가져옴
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 현재 고객 주문

        orderItem = OrderItem.objects.get(order=order, product=product)

        options = ProductOption.objects.get(option_seller_code=seller_code)
        orderItemOption = OrderItemOption.objects.get(order_item_option=orderItem, product_option=options)

        if orderItemOption.quantity == 1 and action == 'remove':  # 화살표로 제품 옵셥 삭제 방지
            pass
        elif action == 'add':
            orderItemOption.quantity = orderItemOption.quantity + 1
        elif action == 'remove':
            orderItemOption.quantity = orderItemOption.quantity - 1

        orderItemOption.save()

        # 변경된 아이템 옵션의 수량, 가격을 return
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
    customer = request.user.customer  # 현재 customer
    product = Product.objects.get(seller_code=seller_code)
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)

    # 옵션이 있을 경우
    if (option == False):
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
        orderItem = OrderItem.objects.get(order=order, product=product)
        option_code = data['optionCode']
        options = ProductOption.objects.get(option_seller_code=option_code)
        orderItemOption = OrderItemOption.objects.get(order_item_option=orderItem, product_option=options)
        orderItemOption.delete()
        data = {
            "orderItemPriceTotal": order.get_total
        }
        itemOption = orderItem.orderitemoption_set.all()
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


"""
제품 배송 체크 api
"""


def checkDelivery(request):
    data = json.loads(request.body)
    settings.sweet_tracker_key
    customer = request.user.customer
    orderHistory = OrderHistory.objects.get(customer=customer, order_number=data['data']['orderNumber'])
    product = Product.objects.get(seller_code=(data['data']['sellerCode']))
    orderItem = OrderItem.objects.get(orderHistory=orderHistory, product=product)

    url = 'https://info.sweettracker.co.kr/api/v1/trackingInfo?t_key=' + settings.sweet_tracker_key + '&t_code=' + str(
        orderItem.deliver_company) + '&t_invoice=' + str(orderItem.track_number)
    # url = 'https://info.sweettracker.co.kr/api/v1/trackingInfo?t_key='+settings.sweet_tracker_key+'&t_code='+str("06")+'&t_invoice='+str(32503569895)
    # level 6 가 완료료

    req = requests.get(url)
    access_res = req.json()
    print(access_res["lastStateDetail"]["level"])

    return render(request, 'error.html')


"""
상품 질문 등록
"""


def productquestion(request):
    data = json.loads(request.body)
    print(data)
    customer = request.user.customer
    product = Product.objects.get(seller_code=data["data"]["sellerCode"])

    if (data["data"]["privacy"] == "public"):
        ProductQuestion.objects.create(product=product, customer=customer
                                       , question_body=data["data"]["question"], question_public=True)
    else:
        ProductQuestion.objects.create(product=product, customer=customer
                                       , question_body=data["data"]["question"], question_public=False)

    msg = "complete"

    json_obj = json.dumps(msg)
    return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


@login_required(login_url='account_login')
def customerservice(request):
    context = {}
    return render(request, 'store/customerservice.html', context)


def faq(request):
    context = {}
    return render(request, 'customerservice/faq.html', context)


@login_required(login_url='account_login')
def onetoone(request):
    context = {}
    return render(request, 'customerservice/onetoonequestion.html', context)


def notice(request):
    context = {}
    return render(request, 'customerservice/notice.html', context)


@login_required(login_url='account_login')
def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html', context)


def checkDeliveryState():
    print("hello")
