from django.urls import path

from . import views

urlpatterns = [
    path('cart', views.cartdetails, name='my_cart' ),
    path('addtocart' ,views.cart , name= 'addcart'),
    path('changeQty/', views.Update_qty, name='increment_quantity'),
    path('remove_to_cart/', views.remove_to_cart, name='remove_to_cart'),
]
