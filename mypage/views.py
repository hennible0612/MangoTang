import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from store.models import OrderHistory, OrderItem, ProductReview, Product

"""
내페이지
"""


@login_required(login_url='account_login')
def mypage(request):
    context = {}
    return render(request, 'store/mypage.html', context)

"""
주문목록
"""
@login_required(login_url='account_login')
def orderhistory(request):
    customer = request.user.customer
    orderHistory = OrderHistory.objects.filter(customer=customer).order_by('-date_completed')

    orderItem = []
    for order in orderHistory:
        orderItem += order.orderitem_set.all()

    context = {'orderHistory': orderHistory, 'orderItem': orderItem}

    return render(request, 'mypage/orderhistory.html', context)


"""
교환환불 신청서
"""
@login_required(login_url='account_login')
def csform(request, orderNumber, sellerCode):
    customer = request.user.customer
    orderHistory = OrderHistory.objects.get(customer=customer, order_number=orderNumber)
    # orderHistory = orderHistory.objects.filter('-date_completed')
    itemData = []
    orderItem = OrderItem.objects.filter(orderHistory=orderHistory)
    for item in orderItem:
        if int(item.product.seller_code) == int(sellerCode):
            itemData = item

    context = {'itemData': itemData}

    return render(request, 'mypage/csform.html', context)


@login_required(login_url='account_login')
def refundlist(request):
    customer = request.user.customer
    orderHistory = OrderHistory.objects.filter(customer=customer)
    orderItem = []
    for order in orderHistory:
        orderItem += order.orderitem_set.all()

    context = {'orderItem': orderItem}
    return render(request, 'mypage/refundlist.html', context)

@login_required(login_url='account_login')
def userinfo(request):
    if request.method == "GET":
        user = request.user
        customer = request.user.customer
        context = {'user': user, 'customer': customer}
        return render(request, 'mypage/userinfo.html', context)
    else:
        data = json.loads(request.body)

        customer = request.user.customer
        customer.post_code = data["data"]["postCode"]
        customer.recipent_address1 = data["data"]["address1"]
        customer.recipent_address2 = data["data"]["address2"]
        customer.save()

        msg = "complete"

        json_obj = json.dumps(msg)
        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})

@login_required(login_url='account_login')
def reviewlist(request):
    customer = request.user.customer
    productReview = ProductReview.objects.filter(customer=customer)

    context = {'productReview': productReview}
    return render(request, 'mypage/reviewlist.html', context)


@login_required(login_url='account_login')
def orderdetail(request, orderNumber, sellerCode):
    customer = request.user.customer
    orderHistory = OrderHistory.objects.filter(customer=customer, order_number=orderNumber)
    product = Product.objects.filter(seller_code=sellerCode)
    orderItem = OrderItem.objects.get(orderHistory__in=orderHistory,
                                      product__in=product)  # 이미 쿼리셋한 쿼리셋으로 쿼리셋을 할려면 __in 필요

    context = {'orderItem': orderItem}
    return render(request, 'mypage/orderdetail.html', context)

@login_required(login_url='account_login')
def reviewform(request, orderNumber, sellerCode):
    customer = request.user.customer
    orderHistory = OrderHistory.objects.get(customer=customer, order_number=orderNumber)
    itemData = []

    if (request.method == "POST"):
        data = json.loads(request.body)
        product = Product.objects.get(seller_code=sellerCode)
        review, created = ProductReview.objects.get_or_create(customer=customer, product=product,
                                                              order_number=orderNumber)
        review.star_rating = int(data["data"]["starRating"])
        review.short_review = str(data["data"]["shortReview"])
        review.long_review = str(data["data"]["longReview"])
        review.save()
        msg = "complete"
        json_obj = json.dumps(msg)
        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        orderItem = OrderItem.objects.filter(orderHistory=orderHistory)
        for item in orderItem:
            if int(item.product.seller_code) == int(sellerCode):
                itemData = item

        context = {'itemData': itemData}
        return render(request, 'mypage/reviewform.html', context)
















"""
----------개발중----------
"""

@login_required(login_url='account_login')
def pointlist(request):
    context = {}
    return render(request, 'mypage/pointlist.html', context)


@login_required(login_url='account_login')
def qnalist(request):
    context = {}
    return render(request, 'mypage/qnalist.html', context)

@login_required(login_url='account_login')
def ordercancel(request):
    context = {}
    return render(request, 'mypage/ordercancel.html', context)


@login_required(login_url='account_login')
def orderrefund(request):
    context = {}
    return render(request, 'mypage/orderrefund.html', context)


# 마이페이지
@login_required(login_url='account_login')
def favoritelist(request):
    context = {}
    return render(request, 'mypage/favoritelist.html', context)


@login_required(login_url='account_login')
def couponlist(request):
    context = {}
    return render(request, 'mypage/couponlist.html', context)