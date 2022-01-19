import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.core import serializers

import io
from rest_framework.parsers import JSONParser
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

    context = {'products': products, 'carousel': carousel, 'carousel_length': carousel_length, 'cartItems':cartItems}

    return render(request, 'store/store.html', context)


def productDetail(request, seller_code):
    product = Product.objects.get(seller_code=seller_code)


    review_page = request.GET.get('page',1) # 리뷰 페이지
    question_page = request.GET.get('page',1) # 리뷰 페이지

    reviews = product.productreview_set.all().order_by('-date_added')
    questions = product.productquestion_set.all().order_by('-date_added')

    #리뷰 페이징
    review_paginator = Paginator(reviews,5)
    review_obj = review_paginator.get_page(review_page)

    # 제품 질문 페이징
    question_paginator = Paginator(questions,5)
    question_obj = question_paginator.get_page(question_page)

    context = {'product': product,'review_page':review_page, 'review_obj':review_obj
        ,'question_page':question_page,'questions':questions,'total_review':len(reviews)
        ,'total_question':len(questions), 'question_obj':question_obj,'reviews':reviews}
    return render(request, 'store/productdetail.html', context)


"""
카트
"""


def cart(request):
    if request.user.is_authenticated:  # 로그인 유저일시
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)
        items = order.orderitem_set.all()  # orderitem은 Order의 자식 그래서 쿼리 가능
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}

    return render(request, 'store/cart.html', context)


def user_login(request):
    context = {}
    return render(request, 'store/login.html', context)


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

            Customer.objects.create(user=user, name=name, email=email, phone_number=phone_number,address1=address1,address2=address2)

            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('store')
    else:
        form = UserForm()

    return render(request, 'store/register.html', {'form': form})


def mypage(request):
    context = {}
    return render(request, 'store/mypage.html', context)


"""
결제 화면
"""


def checkout(request):
    if request.user.is_authenticated:  # 로그인 유저일시
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)
        items = order.orderitem_set.all()  # orderitem은 Order의 자식 그래서 쿼리 가능
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


"""
장바구니에 물품 추가 JSON 응답
"""


def updateItem(request):
    data = json.loads(request.body)  # JSON body data에저장
    productId = data['productId']  # 각각 body에 있는 필요한 값저장
    action = data['action']
    print('Action:', action)  #
    print('Product:', productId)  # 장고 default id 가져옴

    customer = request.user.customer  # 현재 customer
    product = Product.objects.get(id=productId)  # 해당하는 productId가져옴
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)  # 주문객체  만들거나 가져옴 상태 False

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)#해당 orderd와 해당 product를 가지고 있는 orderitem 생성

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save() #DB에 저장

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def getReview(request):
    seller_code = 12312;


    product = Product.objects.get(seller_code=seller_code)
    reviews = product.productreview_set.all().order_by('-date_added')
    # print(data)
    json_obj = serializers.serialize('json', reviews)
    print(json_obj)
    # json_obj = list(reviews)
    return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})





def customerservice(request):
    context = {}
    return render(request, 'store/customerservice.html', context)


def faq(request):
    context = {}
    return render(request, 'customerservice/faq.html', context)


def onetoone(request):
    context = {}
    return render(request, 'customerservice/onetoonequestion.html', context)


def notice(request):
    context = {}
    return render(request, 'customerservice/notice.html', context)


# 주문 관리 view
def orderhistory(request):
    context = {}
    return render(request, 'mypage/orderhistory.html', context)


def ordercancel(request):
    context = {}
    return render(request, 'mypage/ordercancel.html', context)


def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html', context)


# 마이페이지
def favoritelist(request):
    context = {}
    return render(request, 'mypage/favoritelist.html', context)


def couponlist(request):
    context = {}
    return render(request, 'mypage/couponlist.html', context)


def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html', context)


def pointlist(request):
    context = {}
    return render(request, 'mypage/pointlist.html', context)


def qnalist(request):
    context = {}
    return render(request, 'mypage/qnalist.html', context)


def refundlist(request):
    context = {}
    return render(request, 'mypage/refundlist.html', context)


def reviewlist(request):
    context = {}
    return render(request, 'mypage/reviewlist.html', context)


def userinfo(request):
    context = {}
    return render(request, 'mypage/userinfo.html', context)


def orderdetail(request):
    context = {}
    return render(request, 'mypage/orderdetail.html', context)
