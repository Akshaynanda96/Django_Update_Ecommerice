from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404



def cart(request):
    if request.method == 'GET':
        
        user = request.user.is_authenticated
        if not user :
            data = {
                'status': False,
                'message' : 'please login first \n click here http://localhost:8000/accounts/login/'
            }
            return JsonResponse(data)
       
        else :
            get_id = request.GET.get('cart_id')
            get_color = request.GET.get('selectedColor', '')
            get_size = request.GET.get('selectedSize', '')
            product = get_object_or_404(Product, udid=get_id)
            Carts.objects.create(
                user=request.user,
                product=product,
                brand=product.product_Brand,
                artical=product.product_artical,
                size=get_size,
                color=get_color,
                total=product.product_price
            )
            return JsonResponse({'status': 'Succuss'}, status=200)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


    

@login_required(login_url='login')
def cartdetails(request):

    user = request.user    
    addcat = Carts.objects.filter(user = user)

    totalAmt  = 0
    Subtotal = 0
    shipping_charges = 70
    finalAmount = 0
    cat_count = Carts.objects.filter(user = request.user).count()
    cart_products = [ p for p in Carts.objects.all() if p.user == request.user ]

    if cart_products:
        for i in cart_products:
            totalAmt =  i.qty * i.product.product_price
            Subtotal += totalAmt
            finalAmount = Subtotal + shipping_charges

        context = {
            'addcat':addcat,
            'totalAmt':totalAmt,
            'Subtotal':Subtotal,
            'shipping_charges':shipping_charges,
            'finalAmount':finalAmount,
            'cat_count':cat_count,
        }
            
        return render(request , 'cart/cart.html', context)
    
    else:
        return render(request , 'cart/emptycart.html')


def Update_qty(request):

        if request.method == 'GET':
            product_id = request.GET.get('id')
            quantity = request.GET.get('qty')
            price = request.GET.get('price')
            total = 0
            carts = Carts.objects.get(Q(product=product_id) & Q(user = request.user))
            carts.qty = quantity
            total = int(quantity) * int(price)
            carts.total = total
            carts.save()
            cart_products = [ p for p in Carts.objects.all() if p.user == request.user ]
            subtotal = 0
            shippingCharges = 70            
            for i in cart_products:
                subtotal += i.total
            if subtotal >= 1000:
                shippingCharges = 0
                finalAmount = subtotal + shippingCharges
            else:
                shippingCharges = 70
                finalAmount = subtotal + shippingCharges
                
            data = {
                'total': total,
                'subtotal': subtotal,
                'finalAmount': finalAmount,
                'shippingCharges':shippingCharges
            }
            return JsonResponse(data)
        else :
            return JsonResponse({'status': '400'})


def remove_to_cart(request):
    
    if request.method == 'GET':
        prod_id = request.GET.get('uuid')
        print('this is a ',prod_id)
        c = Carts.objects.get(Q(product=prod_id) & Q(user = request.user))    
        c.delete()
        data = {
            'status': '200'
        }
        return JsonResponse(data)
    else:
        data ={
            'status': '400' 
        }
        return JsonResponse(data)
    
    
    
