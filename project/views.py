from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse

from project.models import *
from cart.models import *
from django.db.models import Q

def productsdetails(request, sulg):
 
    try:
        category = get_object_or_404(Category, slugField=sulg)
        products = Product.objects.filter(product_category=category)
        subcategories = SubCategory.objects.filter(products__in=products).distinct()
        user = request.user
        if user.is_authenticated :
            cat_count = Carts.objects.filter(user =user).count()
        else:
            cat_count = 0
       
        context = {
        'subcat':subcategories,
        "products":products,
        "category":category,
        'cat_count':cat_count,
       
        }

        return render(request, 'productdetails/subcat.html', context)

    except Product.DoesNotExist:
        return render(request, 'base/404.html')



def SubCategory_details(request,sulg):
    user = request.user
    if user.is_authenticated :
        cat_count = Carts.objects.filter(user = user).count()
    else:
        cat_count = 0
    subcategory = get_object_or_404(SubCategory, slugField=sulg)
    products = Product.objects.filter(product_subcategory=subcategory)
     
    context = {
        'products': products,
        'cat_count':cat_count,
       
    }

    return render(request, 'productdetails/subshop.html', context)



def itemdetails(request , sulg):
    
    
    user = request.user
    if user.is_authenticated :
        cat_count = Carts.objects.filter(user = user).count()
    else:
        cat_count = 0
    data = get_object_or_404(Product, slugField=sulg)
    item_in_cart = False
    if request.user.is_authenticated:
        item_in_cart  = Carts.objects.filter(Q(user = request.user), Q(product = data.udid ))
        
    context = {
        'data':data,
        'item_in_cart':item_in_cart,
        'cat_count':cat_count,
   
    }
    
    return render(request, 'productdetails/detail.html', context)


def shop( request):
    products = Product.objects.all()
    user = request.user
    if user.is_authenticated :
        cat_count = Carts.objects.filter(user = user).count()
    else:
        cat_count = 0

    
    context = {
        
        'products':products,
        'cat_count':cat_count,
        
    }
    return render(request ,'base/shop.html', context)

    

def pricefilter(request ):
    
    if request.method == 'GET':
        getpricerange = request.GET.get('getpricerange')
       
        if getpricerange:
            if getpricerange == '500':
                products = Product.objects.filter(product_price__gte=0, product_price__lt=500)
            elif getpricerange == '1000':
                products = Product.objects.filter(product_price__gte=500, product_price__lt=1000)
            elif getpricerange == '1500':
                products = Product.objects.filter(product_price__gte=1000, product_price__lt=1500)
            elif getpricerange == '1500-2000':
                products = Product.objects.filter(product_price__gte=1500, product_price__lt=2000)
            elif getpricerange == '5000':
                products = Product.objects.filter(product_price__gte=2000, product_price__lt=5000)
            else:
                products = Product.objects.all()  
        else:
            products = Product.objects.all()  
    

        
        context = {
            'products': products,
        }

        return render(request, 'productdetails/subshop.html', context)
    
    
def updateQty(request):

    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        price = request.GET.get('price')
        new = int(price) * int(quantity)
        cart_item = Carts.objects.get(product_id=product_id, user=request.user)
        cart_item.qty = int(quantity)
        cart_item.total =  round(float(new), 2)
        
        cart_item.save()
    
    return render(request, 'productdetails/detail.html')