import json
from datetime import datetime
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from MangoTang import settings
from store.models import Order, OrderItemOption, OrderHistory, OrderItem, CAExchangeRefundList
import logging

logger = logging.getLogger(__name__)

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


"""
아임포트 토큰 가져오기
api 사용을 위한 토큰 발급
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
결제 화면
"""


@login_required(login_url='account_login')
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    items = order.orderitem_set.all()  # orderitem은 Order의 자식 그래서 쿼리 가능
    cartItems = order.get_cart_items
    itemOption = []
    if (bool(items) == True):
        for item in items:
            itemOption += OrderItemOption.objects.filter(order_item_option=item)

        context = {'items': items, 'order': order, 'cartItems': cartItems, 'itemOption': itemOption,
                   'customer': customer}
        return render(request, 'store/checkout.html', context)
    else:
        return render(request, 'permisson.html')


"""
결제창
"""


def checkoutPayment(request):
    try:
        data = json.loads(request.body)
        customer = request.user.customer  # 현재 customer
        order, created = Order.objects.get_or_create(customer=customer, order_status=False)
        if (order.order_status == False):

            # 결제 정보 order에 저장
            order_id = str(customer.id) + str(datetime.now().timestamp())  # order_id 발급
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

            # 아임포트에 넘겨줄 데이터
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
    except Exception as e:
        logger.critical("exception error: " + str(e) + 'view checkoutPayment 결제 정보 전달 받는 중에 에러')
    return render(request, 'error.html')


"""
결제를 한 후 위조된 결제인지
아닌지를 확인하는 view
"""


def checkoutComplete(request):
    data = json.loads(request.body)
    imp_uid = data['imp_uid']
    merchant_uid = data['merchant_uid']
    try:
        access_res = getToken()  # 토큰 가져오기
    except Exception as e:
        logger.critical("exception error: " + str(e) + 'view checkoutComplete 아임포트 getToken중에러')
        return render(request, 'error.html')

    try:
        iamportData = getPaymentData(access_res, imp_uid)  # 아임포트 서버에서 결제 확인
    except Exception as e:
        logger.critical("exception error: " + str(e) + 'view checkoutComplete 아임포트 getPaymentData중 에러')
        return render(request, 'error.html')

    # 아임포트 서버랑 우리 몰 서버 결제 금액 비교
    IamportAmount = iamportData["response"]["amount"]  # Iamport 서버 결제 금액

    customer = request.user.customer  # 현재 customer
    order, created = Order.objects.get_or_create(customer=customer, order_status=False)
    localAmount = order.get_total + order.get_deliver_price  # 로컬 서버의 결제 금액
    orderhistory = OrderHistory.objects.create(customer=customer)

    orderItem = order.orderitem_set.all()

    if (IamportAmount == localAmount):

        for item in orderItem:
            item.orderHistory = orderhistory
            item.deliver_state = "checking"  # "shipping" "complete"
            item.save()

        # order true로 변경하므로 카트에서 제거
        order.order_status = True
        order.payment_state = True

        # orderhistory에 저장
        orderhistory.order_name = order.get_all_item_name
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
        json_obj = json.dumps(iamportData)
        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:  # 위조시
        iamportData["response"]["status"] = "forgery"
        json_obj = json.dumps(iamportData)

        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})


"""
결제 완료 요약
결제 성공시 주문번호 출력
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
환불 처리
요청된 금액 만큼 환불 처리
"""
def iamportRefundRequest(refundAmount, orderNumber, reason, checkSum):
    token = getToken()

    url = 'https://api.iamport.kr/payments/cancel'
    headers = {
        "Authorization": token
    }
    data = {
        'merchant_uid': orderNumber,
        'amount': refundAmount,
        'checksum': checkSum,  # 총 환불 가능한 금액
        'reason': reason
    }

    req = requests.post(url, headers=headers, data=data)

    access_res = req.json()

    # 성공
    if access_res['code'] == 0:
        return access_res
    else:
        return None


# 주문 취소 요청 받음
def paymentCancel(request):
    return JsonResponse("취소 완료", safe=False, json_dumps_params={'ensure_ascii': False})


"""
환불 요청
iamportRefundRequest() 호출
"""


def reqstExrfn(request):
    data = json.loads(request.body)
    customer = request.user.customer
    reqstExrfn = data["data"]["reqstExrfn"]
    reason = data["data"]["reason"]
    orderNumber = data["data"]["orderNumber"]
    sellerCode = data["data"]["sellerCode"]

    itemData = []
    orderHistory = OrderHistory.objects.get(customer=customer, order_number=orderNumber)
    orderItem = OrderItem.objects.filter(orderHistory=orderHistory)
    for item in orderItem:
        if int(item.product.seller_code) == int(sellerCode):
            itemData = item

    # CAExchangeRefundList 생성
    refundList, created = CAExchangeRefundList.objects.get_or_create(customer=customer, orderItem=itemData)
    refundList.reason = reason
    refundList.rqstExrfn = reqstExrfn
    refundList.date_submitted = datetime.now()

    refundList.save()

    if (str(itemData.deliver_state) == "checking"):
        refundAmount = itemData.get_all_total + itemData.get_delivery_price  # 환불할 총 가격
        checkSum = orderHistory.get_total

        # 환불요청
        response = iamportRefundRequest(refundAmount, orderNumber, reason, checkSum)

        # 환불 성공
        if (response["code"] == 0):

            orderHistory.shipping_fee = orderHistory.shipping_fee - itemData.get_delivery_price
            orderHistory.total_fee = orderHistory.total_fee - itemData.get_all_total
            orderHistory.save()

            itemData.deliver_state = "refunded"
            itemData.save()

            msg = "refundSuccessful"
            json_obj = json.dumps(msg)
            return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            # 환불 과정 중 실패
            msg = "err"
            json_obj = json.dumps(msg)
            return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        # 물품이 배송중이거나 도착 상태일때
        msg = "refundRequestCompleted"

        json_obj = json.dumps(msg)
        return JsonResponse(json_obj, safe=False, json_dumps_params={'ensure_ascii': False})

"""
개발중
"""
def buyNow(request):
    data = json.loads(request.body)  # JSON body data에저장
    customer = request.user.customer
    # order = Order.objects.create(customer=customer, order_status=False)

    context = {'data': data}
    return render(request, 'store/checkout.html', context)
