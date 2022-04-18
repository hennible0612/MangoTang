

from django.urls import path
from . import views

urlpatterns = [
    # 내페이지
    path('mypage/', views.mypage, name="mypage"),
    # 주문내역 페이지
    path('mypage/orderhistory/', views.orderhistory, name="orderhistory"),
    # cs 교화 반품 신청
    path('mypage/orderhistory/cs/<int:orderNumber>/<int:sellerCode>', views.csform, name="cs"),
    path('mypage/ordercancel', views.ordercancel, name="ordercancel"),
    path('mypage/orderrefund', views.orderrefund, name="orderrefund"),
    path('mypage/couponlist', views.couponlist, name="couponlist"),
    path('mypage/favoritelist', views.favoritelist, name="favoritelist"),
    path('mypage/pointlist', views.pointlist, name="pointlist"),
    path('mypage/qnalist', views.qnalist, name="qnalist"),
    path('mypage/refundlist', views.refundlist, name="refundlist"),
    path('mypage/userinfo/', views.userinfo, name="userinfo"),

    # 마이페이지 리뷰리스트
    path('mypage/reviewlist', views.reviewlist, name="reviewlist"),
    path('mypage/orderlist/orderdetail/<int:orderNumber>/<int:sellerCode>', views.orderdetail, name="orderdetail"),
    # 주문번호로 변경
    path('mypage/item/review/<int:orderNumber>/<int:sellerCode>', views.reviewform, name="reviewform"),

]
