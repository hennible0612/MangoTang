from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 결제
    path('checkout/', views.checkout, name="checkout"),
    # 결제 창
    path('checkout/payment/', views.checkoutPayment, name="checkoutPayment"),
    # 결제 완료
    path('checkout/complete/', views.checkoutComplete, name="checkoutComplete"),
    # 결제 완료 요약
    path('checkout/complete/<int:orderId>/', views.checkoutSummery, name="checkoutSummery"),
    # 지금 바로 구매하기
    path('checkout/buynow', views.buyNow, name="buyNow"),

    # 결제 성공
    path('payment/success', views.paymentSuccess, name='paymentSuccess'),
    # 교환 환불 신청
    path('submit/reqstExrfn', views.reqstExrfn, name="reqstExrfn"),
    # 주문 취소
    path('payment/cancel', views.paymentCancel, name="paymentCancel"),
]
