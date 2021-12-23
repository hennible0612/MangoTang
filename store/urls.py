from django.urls import path

from . import views

urlpatterns = [

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('login/', views.login, name="login"),
	path('register/', views.register, name="register"),
	path('mypage/', views.mypage, name="mypage"),
	path('product_detail/<int:seller_code>/', views.product_detail, name="product_detail"), #아이디로 바꾸자
	path('update_item/', views.updateItem, name="update_item"), # 장바구니 추가 요청 url


	path('customerservice/', views.customerservice, name="customerservice"),
	path('customerservice/faq', views.faq, name="faq"),
	path('customerservice/onetoone', views.onetoone, name="onetoone"),
	path('customerservice/notice', views.notice, name="notice"),




	path('mypage/orderhistory', views.orderhistory, name="orderhistory"),
	path('mypage/ordercancel', views.ordercancel, name="ordercancel"),
	path('mypage/orderrefund', views.orderrefund, name="orderrefund"),

	path('mypage/couponlist', views.couponlist, name="couponlist"),
	path('mypage/favoritelist', views.favoritelist, name="favoritelist"),
	path('mypage/pointlist', views.pointlist, name="pointlist"),
	path('mypage/qnalist', views.qnalist, name="qnalist"),
	path('mypage/refundlist', views.refundlist, name="refundlist"),
	path('mypage/userinfo', views.userinfo, name="userinfo"),
	path('mypage/reviewlist', views.reviewlist, name="reviewlist"),


	path('mypage/orderlist/orderdetail', views.orderdetail, name="orderdetail"), #주문번호로 변경

]