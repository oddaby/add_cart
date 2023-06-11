from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product,Order,OrderItem

# Register your models with the admin site
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


