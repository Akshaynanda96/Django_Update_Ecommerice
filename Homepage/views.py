from django.shortcuts import render , redirect
from django.http import JsonResponse
import random
from datetime import timedelta
from django.utils import timezone
from project.models import *
from cart.models import Carts
from django.contrib import messages




def home(request):
    try :

        all_products = list(Product.objects.all())
        if len(all_products) > 8:
            products = random.sample(all_products, 8)
        else:
            products = all_products
# ---------------------------------------------------------------------

        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_products = Product.objects.filter(create_at__gte=thirty_days_ago)
        recent_products = list(recent_products)
        
        if len(recent_products) > 8:
            newproducts = random.sample(recent_products, 8)
        else:
            newproducts = recent_products
     
        category = Category.objects.all()
        categoryheader = Category.objects.all()
        user = request.user
        if user.is_authenticated :
            cat_count = Carts.objects.filter(user = user).count()
        else:
            cat_count = 0
        
        
        context = {
            "data":products,
            'category':category,
            'newproduct':newproducts,
            'all_products':all_products,
            'categoryheader':categoryheader,
            'cat_count':cat_count,               
        }        
        return render(request , 'home/index.html', context)
    except Exception:
        return render(request , 'base/404.html')
    
    

from django.db.models import Q

def search_box(request):
    if request.method == 'GET':
        get_obj = request.GET.get('name_search')
        if get_obj :
            products = Product.objects.filter(
                Q(product_name__icontains=get_obj) |
                Q(product_category__category_name__icontains=get_obj) |
                Q(product_subcategory__subcategory_name__icontains=get_obj) |
                Q(product_Brand__icontains=get_obj) |
                Q(product_artical__icontains=get_obj)
            ).distinct()
            
            if products:
                context = {
                    'products': products,
                }
                return render(request, 'base/shop.html', context)
            
            else:
                messages.info(request, 'No products found')
                print('No products found')
                return redirect('home')
                
        else:
            messages.info(request, 'Please Enter to Search')
            return redirect('home')
    
    return render(request, 'base/shop.html')  

def Discount(request, slug):
    try:
        discount_percentage = int(slug)  # Convert slug to integer
        products = Product.objects.filter(product_dicount = discount_percentage)
        context = {
            'products': products,
        }
        return render(request, 'home/discount.html', context)
    except ValueError:
        # Handle cases where slug is not a valid integer (optional)
        return render(request, 'home/error.html', {'message': 'Invalid discount percentage provided.'})

    
    
    