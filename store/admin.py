from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Carosel)
admin.site.register(ProductReview)
admin.site.register(ProductQuestion)
admin.site.register(ProductOption)
admin.site.register(OrderItemOption)

