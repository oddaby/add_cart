from django.urls import path
from . import views

urlpatterns = [
    # path(route, view, name)
    path('products/', views.products, name='products'),
    path('', views.customer_login, name='login'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_summary/', views.order_summary, name='order_summary'),


    # add more paths as needed
]
