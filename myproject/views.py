from django.shortcuts import render,HttpResponse,redirect
from myapp.EmailBackend import EmailBackend 
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import CustomUser,Customer,Help,contactus
def LOGIN(request):
    return render(request,'login.html')
def do_login(request):
    if request.method == 'POST':
        user = EmailBackend().authenticate(
            request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == 1:
                return redirect('admin_home')
            elif user_type == 2:
                return redirect('customer_home')
            else:
                messages.error(request, 'Email and password are Invalid')
                return redirect('login') 
        else:
            messages.error(request, 'Email and password are Invalid')
            return redirect('login') 
    else:
        messages.error(request, 'Invalid request method')
        return redirect('login')
    
def do_logout(request):
    logout(request)
    return redirect('login')
@login_required(login_url='/')
def profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    user2=Customer.objects.get(id=request.user.id)
    return render(request,'profile.html',{'user':user,'user2':user2})  
@login_required(login_url='/')
def profile_update(request):
    if request.method == 'POST':
        profile_pic= request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        address=request.POST.get('address')
        mobile_no=request.POST.get('mobile_no')
        # email=request.POST.get('email')
        # username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            
            if password !=None and password !="":  
              customuser.set_password(password)
            if profile_pic !=None and profile_pic !="":  
              customuser.profile_pic=profile_pic
            customuser.save()
            customer=Customer.objects.get(id=request.user.id-1)
            if address:
             customer.address=address
            if mobile_no:
             customer.mobile_no=mobile_no
            customer.save()
            messages.success(request,'your Profile Update Sucessfully')  
            return redirect('profile')
            
        except :
            messages.error(request,'Profile Update Failed')
            return redirect('profile')
    return render(request,'profile.html') 
def contacus(request):
    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name=request.POST.get('name')
        email=request.POST.get('email')
        description=request.POST.get('description')
        print(name,email,description)
        if not (name and email  and description):
            return HttpResponseBadRequest("All fields are required")
        help=contactus(
            customer_id=customer,
            name=name,
            email=email,
            description=description
        )
        help.save()
        return render(request,"contactus.html")
    return render(request,"contactus.html")
def termandcondition(request):
    return render(request,"includes/termandcondition.html")
def help(request):
    return render(request,'help.html')
def help_apply(request):
    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        description=request.POST.get('description')
        print(name,email,mobile_no,description)
        if not (name and email and mobile_no and description):
            return HttpResponseBadRequest("All fields are required")
        help=Help(
            customer_id=customer,
            name=name,
            mobile_no=mobile_no,
            email=email,
            description=description
        )
        help.save()
        return render(request,'helpapply.html')
    return render(request,'helpapply.html')
def myprofile(request):
    customuser = request.user
    print(customuser.user_type)
    
    user2=Customer.objects.get(id=customuser.id)  
    return render(request,'myprofile.html',{'user':customuser,'user2':user2})
def aboutus(request):
    return render(request,'aboutus.html')
def privicypolicy(request):
    return render(request,'privecypolicy.html')
def shiping(request):
    return render(request,'shiping.html')
def refundcancel(request):
    return render(request,'refundandcancel.html')                