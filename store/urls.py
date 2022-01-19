from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name="login"),
	path('register/', views.register, name="register"),
	path('mypage/', views.mypage, name="mypage"),
	path('productDetail/<int:seller_code>/', views.productDetail, name="product_detail"),

	path('get_review/', views.getReview, name="get_review"), #

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