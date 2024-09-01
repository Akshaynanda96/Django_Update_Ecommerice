from django.shortcuts import render , HttpResponse

def wishlist(request):
    
    return render(request , 'wishList/wishlist.html')
