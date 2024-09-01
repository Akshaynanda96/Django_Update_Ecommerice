from django.shortcuts import render ,redirect
from django.http import HttpResponseRedirect ,HttpResponse
from accounts.models import Profile ,profileDetails ,STATE_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth import login , logout ,authenticate 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Carts

def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request , "This Email id is not registered")
            return  HttpResponseRedirect(request.path)
    
        user_obj = authenticate(username = email , password= password)
    
        if user_obj:
            login(request, user_obj)
            return redirect ("/")
    
        messages.warning(request, "Invalided Password")
    return render(request , 'accounts/login.html')


def user_logout(request):
        logout(request)
        return redirect('login')
  

def registration_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists() :
            messages.error(request , "this user is already exists")
            return  HttpResponseRedirect(request.path)
        
        else:
            user_obj = User.objects.create(
                username = email,
                first_name = first_name,
                last_name = last_name,
                email = email,
            )
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request , "Verification link Sent on your Registration Email Id")
        
    return render(request , 'accounts/register.html')


def email_active(request , email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.email_verifcation = True
        user.save()
        return redirect("/")
    
    except Exception as ex:
        return HttpResponse("invalided token")
    
@login_required(login_url='/accounts/login')
def profile_D(request):
    cat_count = Carts.objects.filter(user = request.user).count()
    user = request.user
    context = {  
        'state_choices': STATE_CHOICES,
        "user":user,
        'cat_count':cat_count,
    }   
    if request.method == 'POST':
        user = request.user
        fname = request.POST.get('f_name')
        Lname = request.POST.get('l_name')
        Address =request.POST.get('Address')   
        City =request.POST.get('City')
        state = request.POST.get('state')
        zip =request.POST.get('zip')
        profile_image = request.FILES.get('profile_image')

        if not (fname and Lname and Address and City and state and zip):
            messages.error(request, 'All fields are required.')

        else: 
            obj = profileDetails.objects.create(
                user = user,
                First_name = fname,
                Last_name  = Lname,
                city_name = City,
                sate_name = state,
                Addresses = Address,
                pincode = zip,
                profile_image = profile_image,
            )
            obj.save()
            messages.success(request, 'Successfully Save Details')
            return redirect ('profile')


    return render(request, 'accounts/profile.html', context)



def contact(request):
    user = request.user
    if user.is_authenticated :
        cat_count = Carts.objects.filter(user).count()
    else:
        cat_count = 0
    context= {
        'cat_count':cat_count,
    }
    return render(request , 'base/contact.html', context)
