from django.urls import path

from . import views

urlpatterns = [

	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('product_detail/', views.product_detail, name="product_detail"), #아이디로 바꾸자

]