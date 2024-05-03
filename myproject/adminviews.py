from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from myapp.models import CustomUser,Help,contactus,Customer,SetKeys,JobCardPdf,DetailsToPdf,FindRcPdf,FindPmKishanPaymentDetails,FindAyushmanCardPdf,FindDlNumber,DLPdf,PMKishanRegistrationNumber,RashanNumbertoUid,MatchAadharNumber,PanManualPdf,MatchAadharCardToPDf,EidtoUid,FindPanCard,IncomeCertificate,DomicalCertificate,FindAadharCard,UidToPdf
from django.contrib import messages
from datetime import date
@login_required(login_url='/')
def home(request):
    customer_count=Customer.objects.all().count()
    pan_manualpdfcount = PanManualPdf.objects.filter(status=0).count()
    findpancardcount=FindPanCard.objects.filter(status=0).count()
    incomecertificate=IncomeCertificate.objects.filter(status=0).count()
    domicalcertificate=DomicalCertificate.objects.filter(status=0).count()
    findaadharcard=FindAadharCard.objects.filter(status=0).count()
    uidtopdf=UidToPdf.objects.filter(status=0).count()
    eidtouid=EidtoUid.objects.filter(status=0).count()
    matchaadharcardtopdf=MatchAadharCardToPDf.objects.filter(status=0).count()
    matchAadharNumber=MatchAadharNumber.objects.filter(status=0).count()
    rashanNumbertoUid=RashanNumbertoUid.objects.filter(status=0).count()
    pMKishanRegistrationNumber=PMKishanRegistrationNumber.objects.filter(status=0).count()
    dLPdf=DLPdf.objects.filter(status=0).count()
    findDlNumber=FindDlNumber.objects.filter(status=0).count()
    findAyushmanCardPdf=FindAyushmanCardPdf.objects.filter(status=0).count()
    findPmKishanPaymentDetails=FindPmKishanPaymentDetails.objects.filter(status=0).count()
    findRcPdf=FindRcPdf.objects.filter(status=0).count()
    context = {
        'customer_count': customer_count,
        'pan_manualpdfcount':pan_manualpdfcount,
        'findpancardcount':findpancardcount,
        'incomecertificate':incomecertificate,
        'domicalcertificate':domicalcertificate,
        'findaadharcard':findaadharcard,
        'uidtopdf':uidtopdf,
        'eidtouid':eidtouid,
        'matchaadharcardtopdf':matchaadharcardtopdf,
        'matchAadharNumber':matchAadharNumber,
        'rashanNumbertoUid':rashanNumbertoUid,
        'pMKishanRegistrationNumber':pMKishanRegistrationNumber,
        'dLPdf':dLPdf,
        'findAyushmanCardPdf':findAyushmanCardPdf,
        'findDlNumber':findDlNumber,
        'findPmKishanPaymentDetails':findPmKishanPaymentDetails,
        'findRcPdf':findRcPdf,
    }
    return render(request,'Admin/home.html',context)
@login_required(login_url='/')
def add_customer(request):
    if request.method == 'POST':
        profile_pic= request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        mobile_no=request.POST.get('mobile_no')
        address=request.POST.get('address')
        password=request.POST.get('password')
        print(profile_pic,first_name,last_name,email,username,mobile_no,address,password)
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exists')
            return redirect('add_customer')
        if CustomUser.objects.filter(username=username).exists(): 
            messages.warning(request,'Username already exists')
            return redirect('add_customer')
        else:
            user=CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                user_type=2
            )       
            user.set_password(password)
            user.save()
            customer=Customer(
                admin=user,
                address=address,
                mobile_no=mobile_no,
            )
            customer.save()
            messages.success(request,user.first_name+" " + user.last_name +" Sucessfully added")
            return redirect('add_customer')
            
        return redirect('add_customer')  
    return render(request, 'Admin/addcustomer.html')
@login_required(login_url='/')
def view_all_customer(request):
    customer=Customer.objects.all()
    print(customer)
    return render(request,'Admin/viewallcustomer.html',{'customer':customer})

@login_required(login_url='/')    
def edit_customer(request,id):
    customer=Customer.objects.filter(id=id)
    context = {
        'customer': customer,
    }
    return render(request,'Admin/edit_customer.html',context)
@login_required(login_url='/')
def update_customer(request):
    if request.method == 'POST':
        customer_id=request.POST.get('customer_id')
        profile_pic= request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        mobile_no=request.POST.get('mobile_no')
        address=request.POST.get('address')
        password=request.POST.get('password')
        user=CustomUser.objects.get(id=customer_id)
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.usernmae=username
        if password !=None and password !="":  
              user.set_password(password)
        if profile_pic !=None and profile_pic !="":  
             user.profile_pic=profile_pic
        user.save()
        customer= Customer.objects.get(admin=customer_id)
        customer.address=address
        customer.mobile_no=mobile_no
        customer.save()
        messages.success(request,user.first_name+" "+ user.last_name+" Update Sucessfully")
        return redirect('update_customer')     
    return render(request,'Admin/edit_customer.html')
@login_required(login_url='/')
def customer_delete(request,id):
    customer = CustomUser.objects.get(id=id)
    customer.delete()
    messages.success(request,"Customer are Delete Sucessfully")
    return redirect('view_all_customer')
@login_required(login_url='/')
def view_all_pan_manual(request):
    customer=PanManualPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/pancardmanualpdf.html',{'customer':customer})  
@login_required(login_url='/')  
def pan_manual_delete(request,id):
    pandetail = PanManualPdf.objects.get(id=id)
    pandetail.delete()
    messages.success(request,"Pan  Detail are Delete Sucessfully")
    return redirect('all_pan_manual')
@login_required(login_url='/')
def edit_pan_manual_pdf(request,id):
    pan_manual_pdf=PanManualPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_pan_manual.html',context)
@login_required(login_url='/')
def update_pan_manual_pdf(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        upload_file = request.FILES.get('upload_file')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
        print(customer_id)  # Ensure customer_id is being correctly printed
        
        pan_manual_pdf = PanManualPdf.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('update_pan_manual_pdf')
    return render(request, 'Admin/edit_pan_manual.html')
@login_required(login_url='/')
def view_all_pan_number_list(request):
    customer=FindPanCard.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/findpancardlist.html',{'customer':customer})
@login_required(login_url='/')
def pan_number_delete(request,id):
    pandetail = FindPanCard.objects.get(id=id)
    pandetail.delete()
    messages.success(request,"Pan  Detail are Delete Sucessfully")
    return redirect('all_pan_number_list')
@login_required(login_url='/')
def edit_pan_number(request,id):
    pan_manual_pdf=FindPanCard.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_find_pan_number.html',context)
@login_required(login_url='/')
def update_pan_number(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        pan_number=request.POST.get('pan_number')
        customer_id = request.POST.get('customer_id')
        pan_number_detail = FindPanCard.objects.get(id=customer_id)
        pan_number_detail.status=status
        pan_number_detail.prev_date=prev_date
        pan_number_detail.pan_number=pan_number
        pan_number_detail.save()
        messages.success(request,'Your Detail Update Sucessfully')
        print(status,pan_number,customer_id)
        return redirect('update_pan_number')
    return render(request, 'Admin/edit_find_pan_number.html')
@login_required(login_url='/')
        
def  view_all_income_list(request):
    customer=IncomeCertificate.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/incomecertificatelist.html',{'customer':customer})
@login_required(login_url='/')
def income_certificate_delete(request,id):
    incomedetail = IncomeCertificate.objects.get(id=id)
    incomedetail.delete()
    messages.success(request,"Pan  Detail are Delete Sucessfully")
    return redirect('all_income_detail')
@login_required(login_url='/')
def edit_income_certificate(request,id):
    pan_manual_pdf=IncomeCertificate.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_income_certificate.html',context)
@login_required(login_url='/')
def update_income_detail(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        download_file=request.FILES.get('download_file')
        customer_id = request.POST.get('customer_id')
        income_details = IncomeCertificate.objects.get(id=customer_id)
        income_details.status=status
        income_details.prev_date=prev_date
        income_details.download_file=download_file
        income_details.save()
        messages.success(request,'Your Detail Update Sucessfully')
        print(status,customer_id,download_file)
        return redirect('update_pan_number')
    return render(request, 'Admin/edit_income_certificate.html')
@login_required(login_url='/')
def  view_all_domical_list(request):
    customer=DomicalCertificate.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/domicalcertificatelist.html',{'customer':customer})
@login_required(login_url='/')
def domical_certificate_delete(request,id):
    domicaldetail = DomicalCertificate.objects.get(id=id)
    domicaldetail.delete()
    messages.success(request,"Pan  Detail are Delete Sucessfully")
    return redirect('all_domical_detail')
@login_required(login_url='/')
def edit_domical_certificate(request,id):
    pan_manual_pdf=DomicalCertificate.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_domical_certificate.html',context)
@login_required(login_url='/')
def update_domical_detail(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        download_file=request.FILES.get('download_file')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
        income_details = DomicalCertificate.objects.get(id=customer_id)
        income_details.status=status
        income_details.download_file=download_file
        income_details.prev_date=prev_date
        income_details.save()
        messages.success(request,'Your Detail Update Sucessfully')
        print(status,customer_id,download_file)
        return redirect('update_domical_detail')
    return render(request, 'Admin/edit_domical_certificate.html')
@login_required(login_url='/')

def view_all_aadhar_number_list(request):
    customer=FindAadharCard.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/findaadharcardlist.html',{'customer':customer})
@login_required(login_url='/')
def aadhar_number_delete(request,id):
    aadhardetail = FindAadharCard.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"Aadhar  Detail are Delete Sucessfully")
    return redirect('all_aadhar_manual')
@login_required(login_url='/')
def edit_aadhar_number(request,id):
    pan_manual_pdf=FindAadharCard.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_find_aadhar_to_pan.html',context)
@login_required(login_url='/')
def update_aadhar_number(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        aadhar_number=request.POST.get('aadhar_number')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
        pan_number_detail = FindAadharCard.objects.get(id=customer_id)
        pan_number_detail.status=status
        pan_number_detail.prev_date=prev_date
        pan_number_detail.aadhar_number=aadhar_number
        pan_number_detail.save()
        messages.success(request,'Your Detail Update Sucessfully')
        return redirect('update_aadhar_number')
    return render(request, 'Admin/edit_find_aadhar_to_pan.html')
@login_required(login_url='/')
def view_all_uid_list(request):
    customer=UidToPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/uidtopdflist.html',{'customer':customer})
@login_required(login_url='/')
def uid_pdf_delete(request,id):
    aadhardetail = UidToPdf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"UID  Detail are Delete Sucessfully")
    return redirect('all_uid_list')
@login_required(login_url='/')
def edit_uid_pdf(request,id):
    pan_manual_pdf=UidToPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_uid_to_pdf.html',context)
@login_required(login_url='/')
def update_uid_to_pdf(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        upload_file = request.FILES.get('upload_file')
        customer_id = request.POST.get('customer_id')
        print(customer_id)  # Ensure customer_id is being correctly printed
        
        pan_manual_pdf = UidToPdf.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('update_uid_to_pdf')
    return render(request, 'Admin/edit_uid_to_pdf.html')
@login_required(login_url='/')
def view_all_eid_list(request):
    customer=EidtoUid.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    
    return render(request,'Admin/eidtouidlist.html',{'customer':customer})
@login_required(login_url='/')
def eid_to_uid_delete(request,id):
    aadhardetail = EidtoUid.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"UID  Detail are Delete Sucessfully")
    return redirect('all_eid_list')
@login_required(login_url='/')
def edit_eid_to_uid(request,id):
    pan_manual_pdf=EidtoUid.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_eid_to_uid.html',context)
@login_required(login_url='/')
def update_eid_to_uid(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        uid = request.POST.get('uid')
        customer_id = request.POST.get('customer_id')
        print(customer_id)  # Ensure customer_id is being correctly printed
        
        pan_manual_pdf = EidtoUid.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.uid=uid
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('update_eid_to_uid')
    return render(request, 'Admin/edit_eid_to_uid.html')
@login_required(login_url='/')
def view_all_matching_aadhar_list(request):
    
    customer=MatchAadharCardToPDf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/matchingaadharlist.html',{'customer':customer})
@login_required(login_url='/')
def matching_aadhar_pdf_delete(request,id):
    aadhardetail =  MatchAadharCardToPDf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"UID  Detail are Delete Sucessfully")
    return redirect('view_all_matching_aadhar_list')   
@login_required(login_url='/')
def edit_matching_aadhar_duplicate(request,id):
    pan_manual_pdf=MatchAadharCardToPDf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_matching_aadhar_card_to_pdf.html',context) 
@login_required(login_url='/')
def matching_aadhar_to_pdf_save(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        upload_file = request.FILES.get('download_file')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
        print(customer_id)  # Ensure customer_id is being correctly printed
        pan_manual_pdf = MatchAadharCardToPDf.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('matching_aadhar_to_pdf_save')
    return render(request, 'Admin/edit_matching_aadhar_card_to_pdf.html')
@login_required(login_url='/')

def view_all_matching_aadhar_number_list(request):
        
    customer=MatchAadharNumber.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/matchingaadharcardtonumberlist.html',{'customer':customer})
@login_required(login_url='/')
def matching_aadhar_number_delete(request,id):
    aadhardetail =  MatchAadharNumber.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"UID  Detail are Delete Sucessfully")
    return redirect('view_all_matching_aadhar_number_list')  
@login_required(login_url='/')
def edit_matching_aadhar_duplicate_number(request,id):
    pan_manual_pdf=MatchAadharNumber.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_matching_aadhar_card_to_number.html',context) 
@login_required(login_url='/')
def matching_aadhar_to_number_save(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        upload_number = request.POST.get('upload_number')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
        print(customer_id,upload_number,status)  # Ensure customer_id is being correctly printed
        pan_manual_pdf = MatchAadharNumber.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_number=upload_number
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('matching_aadhar_to_number_save')
    return render(request, 'Admin/edit_matching_aadhar_card_to_number.html')
@login_required(login_url='/')
def view_all_rashan_list(request):
    customer=RashanNumbertoUid.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/rashannumberlist.html',{'customer':customer})
@login_required(login_url='/')
def eid_to_rashan_delete(request,id):
    aadhardetail =  RashanNumbertoUid.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"UID  Detail are Delete Sucessfully")
    return redirect('view_all_rashan_list')  
@login_required(login_url='/')
def edit_rashan_number_uid(request,id):
    pan_manual_pdf=RashanNumbertoUid.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_rashan_number_to_uid.html',context)
@login_required(login_url='/')
def rashan_number_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        uid= request.POST.get('uid')
        customer_id = request.POST.get('customer_id')
        print(customer_id,uid,status)  # Ensure customer_id is being correctly printed
        pan_manual_pdf = RashanNumbertoUid.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.uid=uid
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('rashan_number_update')
    return render(request, 'Admin/edit_rashan_number_to_uid.html')
@login_required(login_url='/')
def view_all_pm_kishan_registration_list(request):
    customer=PMKishanRegistrationNumber.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/pmkishanregistrationnumberlist.html',{'customer':customer})
@login_required(login_url='/')
def pm_kishan_registration_number_delete(request,id):
    aadhardetail =  PMKishanRegistrationNumber.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"UID  Detail are Delete Sucessfully")
    return redirect('view_all_pm_kishan_registration_list')  
@login_required(login_url='/')
def edit_pm_kishan_registration_number(request,id):
    pan_manual_pdf=PMKishanRegistrationNumber.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_kishan_registration_number.html',context)
@login_required(login_url='/')
def pm_kishan_registration_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        kishan_registration_number= request.POST.get('kishan_registration_number')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = PMKishanRegistrationNumber.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.kishan_registration_number=kishan_registration_number
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('pm_kishan_registration_update')
    return render(request, 'Admin/edit_kishan_registration_number.html')
@login_required(login_url='/')
def view_all_dl_pdf_list(request):
    customer=DLPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/dlpdfadminlist.html',{'customer':customer})
@login_required(login_url='/')
def dl_pdf_delete(request,id):
    aadhardetail =  DLPdf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"DL Detail are Delete Sucessfully")
    return redirect('view_all_dl_pdf_list')
@login_required(login_url='/')
def edit_dl_pdf(request,id):
    pan_manual_pdf=DLPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_dl_pdf.html',context)
@login_required(login_url='/')
def dl_pdf_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        upload_file = request.FILES.get('upload_file')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = DLPdf.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('dl_pdf_update')
    return render(request, 'Admin/edit_dl_pdf.html')
@login_required(login_url='/')
def view_all_find_dl_number_list(request):
    customer=FindDlNumber.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/finddlnumberlist.html',{'customer':customer})
@login_required(login_url='/')
def find_dl_number_delete(request,id):
    aadhardetail =  FindDlNumber.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"DL Detail are Delete Sucessfully")
    return redirect('view_all_find_dl_number_list')
@login_required(login_url='/')
def edit_find_dl_number(request,id):
    pan_manual_pdf=FindDlNumber.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_find_dl_number.html',context)
@login_required(login_url='/')
def find_dl_number_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        upload_dl_number = request.POST.get('upload_dl_number')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = FindDlNumber.objects.get(id=customer_id)
        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_dl_number=upload_dl_number
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('find_dl_number_update')
    return render(request, 'Admin/edit_find_dl_number.html')
@login_required(login_url='/')
def view_all_ayushman_card_download_list(request):
    customer=FindAyushmanCardPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/findayushmancardlist.html',{'customer':customer})
@login_required(login_url='/')
def find_ayushman_card_delete(request,id):
    aadhardetail =  FindAyushmanCardPdf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"DL Detail are Delete Sucessfully")
    return redirect('view_all_ayushman_card_download_list')
@login_required(login_url='/')
def edit_ayushman_card_download(request,id):
    pan_manual_pdf=FindAyushmanCardPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_find_ayushman_card_download.html',context)
@login_required(login_url='/')
def ayushman_card_download_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        upload_file = request.FILES.get('upload_file')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = FindAyushmanCardPdf.objects.get(id=customer_id)

        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('ayushman_card_download_update')
    return render(request, 'Admin/edit_find_ayushman_card_download.html')
@login_required(login_url='/')
def view_all_pm_kishan_payment_details(request):
    customer=FindPmKishanPaymentDetails.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/findpmkishanpaymentdetails.html',{'customer':customer})
@login_required(login_url='/')
def find_pm_kishan_payment_delete(request,id):
    aadhardetail =  FindPmKishanPaymentDetails.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"DL Detail are Delete Sucessfully")
    return redirect('view_all_pm_kishan_payment_details')
@login_required(login_url='/')
def edit_pm_kishan_payment_details(request,id):
    pan_manual_pdf=FindPmKishanPaymentDetails.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_find_kishan_payment_details.html',context)
@login_required(login_url='/')
def pm_kishan_payment_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        upload_file = request.FILES.get('upload_file')
        prev_date=request.POST.get('prev_date')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = FindPmKishanPaymentDetails.objects.get(id=customer_id)

        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('pm_kishan_payment_update')
    return render(request, 'Admin/edit_find_kishan_payment_details.html')
@login_required(login_url='/')
def view_all_rc_pdf_list(request):
    customer=FindRcPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/findrcpdflist.html',{'customer':customer})
@login_required(login_url='/')
def rc_pdf_delete(request,id):
    aadhardetail =  FindRcPdf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"DL Detail are Delete Sucessfully")
    return redirect('view_all_rc_pdf_list')
@login_required(login_url='/')
def edit_rc_pdf_details(request,id):
    pan_manual_pdf=FindRcPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_rc_pdf.html',context)
@login_required(login_url='/')
def rc_pdf_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date')
        upload_file = request.FILES.get('upload_file')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = FindRcPdf.objects.get(id=customer_id)

        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('rc_pdf_update')
    return render(request, 'Admin/edit_rc_pdf.html')
@login_required(login_url='/')
def view_all_details_to_list(request):
    customer=DetailsToPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/detailstopdflist.html',{'customer':customer})
@login_required(login_url='/')
def details_pdf_delete(request,id):
    aadhardetail =  DetailsToPdf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"Details to Pdf Detail are Delete Sucessfully")
    return redirect('view_all_details_to_list')
@login_required(login_url='/')
def edit_details_pdf(request,id):
    pan_manual_pdf=DetailsToPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_details_pdf.html',context)
@login_required(login_url='/')
def details_pdf_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        upload_file = request.FILES.get('upload_file')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        prev_date=request.POST.get('prev_date') 
        pan_manual_pdf = DetailsToPdf.objects.get(id=customer_id)

        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('details_pdf_update')
    return render(request, 'Admin/edit_details_pdf.html')
@login_required(login_url='/')
def view_all_job_card_pdf_list(request):
    customer=JobCardPdf.objects.all()
    current_date = date.today()
    for c in customer:
        if c.prev_date:  
            c.days = (current_date - c.prev_date).days
            if c.days>=7:
                c.is_valid=True
            c.save()
    return render(request,'Admin/jobcardpdflist.html',{'customer':customer})
@login_required(login_url='/')
def job_card_pdf_delete(request,id):
    aadhardetail =  JobCardPdf.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"Job card  Detail are Delete Sucessfully")
    return redirect('view_all_job_card_pdf_list')
@login_required(login_url='/')
def edit_job_card_pdf(request,id):
    pan_manual_pdf=JobCardPdf.objects.get(id=id)
    context = {
        'customer': pan_manual_pdf,
        'edit_update':id
    }
    return render(request,'Admin/edit_job_card_pdf.html',context)
@login_required(login_url='/')
def jobcard_pdf_update(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        prev_date=request.POST.get('prev_date') 
        upload_file = request.FILES.get('upload_file')
        customer_id = request.POST.get('customer_id')
         # Ensure customer_id is being correctly printed
        pan_manual_pdf = JobCardPdf.objects.get(id=customer_id)

        pan_manual_pdf.status=status
        pan_manual_pdf.prev_date=prev_date
        pan_manual_pdf.upload_file=upload_file
        pan_manual_pdf.save()
        messages.success(request,'Your Detail Update sucessfully')
        return redirect('jobcard_pdf_update')
    return render(request, 'Admin/edit_job_card_pdf.html')
@login_required(login_url='/')
def set_key(request):
    show_key=SetKeys.objects.first()
    
    return render(request,'Admin/set_key.html',{'key':show_key})
@login_required(login_url='/')
def edit_key(request):
    return render(request,'Admin/edit_key.html',)
@login_required(login_url='/')
def edit_key_update(request):
    if request.method == 'POST':
        key_id=request.POST.get('key_id')
        secret_key=request.POST.get('secret_key')
        print(key_id,secret_key)
        set_key_data=SetKeys.objects.get(id=1)
        set_key_data.key_id=key_id
        set_key_data.secret_key=secret_key
        set_key_data.save()
        return redirect('update_key')
    return render(request, 'Admin/edit_key.html')
@login_required(login_url='/')
def view_all_help(request):
    customer=Help.objects.all()
    return render(request,'Admin/helplist.html',{'customer':customer})
@login_required(login_url='/')
def help_delete(request,id):
    aadhardetail =  Help.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"Help  Detail are Delete Sucessfully")
    return redirect('view_all_help')
def view_all_contact(request):
    customer=contactus.objects.all()
    return render(request,'Admin/contactlist.html',{'customer':customer})
@login_required(login_url='/')
def contactus_delete(request,id):
    aadhardetail =  contactus.objects.get(id=id)
    aadhardetail.delete()
    messages.success(request,"Contact  Detail are Delete Sucessfully")
    return redirect('view_all_contact')

