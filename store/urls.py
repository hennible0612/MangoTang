from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	#로그아웃 요청
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	#로그인 요청
	path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name="login"),
	# 장바구니에 추가 요청
	path('update_item/', views.updateItem, name="update_item"),
	# 장바구니에 추가 요청
	path('update-cart-item/', views.updateCartItem, name="update_cart_item"),
	# 장바구니에 추가 요청
	path('delete-cart-item/<int:seller_code>/', views.deleteCartItem, name="delete_cart_item"),

	# 메인화면
	path('', views.store, name="store"),
	# 카트
	path('cart/', views.cart, name="cart"),
	# 결제
	path('checkout/', views.checkout, name="checkout"),
	#회원가입
	path('register/', views.register, name="register"),

	#제품 상세페이지
	path('productDetail/<int:seller_code>/', views.productDetail, name="product_detail"),
	#제품 리뷰 API
	path('product/review/<int:seller_code>/<int:page>/', views.getReview, name="getReview"),

	#결제 창
	path('checkout/payment/', views.checkoutPayment, name="checkoutPayment"),
	#결제 완료
	path('checkout/complete/', views.checkoutComplete, name="checkoutComplete"),
	#결제 완료 요약
	path('checkout/complete/<int:orderId>/', views.checkoutSummery, name="checkoutSummery"),

	# 제품 문의 API
	path('product/question/<int:seller_code>/<int:page>/', views.getQuestion, name="getQuestion"),

	# 결제 성공
	path('payment/success',views.paymentSuccess, name='paymentSuccess'),


	# 내페이지
	path('mypage/', views.mypage, name="mypage"),

	path('customerservice/', views.customerservice, name="customerservice"),
	path('customerservice/faq', views.faq, name="faq"),
	path('customerservice/onetoone', views.onetoone, name="onetoone"),
	path('customerservice/notice', views.notice, name="notice"),
	# 주문내역 페이지
	path('mypage/orderhistory/', views.orderhistory, name="orderhistory"),
	# cs 교화 반품 신청
	path('mypage/orderhistory/cs/<int:orderNumber>', views.csform, name="cs"),

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