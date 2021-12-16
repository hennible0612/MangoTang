from django.urls import path

from . import views

urlpatterns = [

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('login/', views.login, name="login"),
	path('register/', views.register, name="register"),
	path('mypage/', views.mypage, name="mypage"),
	path('product_detail/', views.product_detail, name="product_detail"), #아이디로 바꾸자




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

]