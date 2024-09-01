from django.urls import path
from . import views

urlpatterns = [
    path('wishList/',views.wishlist, name='wishList')
]