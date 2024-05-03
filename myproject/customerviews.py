from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from myapp.models import CustomUser,AmountSet,SetKeys,DetailsToPdf,JobCardPdf,FindRcPdf,FindPmKishanPaymentDetails,FindAyushmanCardPdf,FindDlNumber,Customer,DLPdf,PMKishanRegistrationNumber,RashanNumbertoUid,MatchAadharNumber,MatchAadharCardToPDf,PanManualPdf,FindPanCard,IncomeCertificate,DomicalCertificate,FindAadharCard,UidToPdf,EidtoUid
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
import razorpay
from django.views.decorators.csrf import csrf_exempt
@login_required(login_url='/')
def home(request):
    return render(request,'Customer/home.html')
@login_required(login_url='/')
def PanCardManualPdf(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/pancardmanualpdf.html',{'amount':amount})
@login_required(login_url='/')
def PanCardManualPdflist(request):
     # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # Filter PanManualPdf objects based on the associated Customer object
    pan_manual_pdfs = PanManualPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/pancardmanualpdflist.html',{'customer':pan_manual_pdfs})
@login_required(login_url='/')
def PanCardManualPdfsave(request):
    if request.method == 'POST':
        # Retrieve or create a Customer object for the current user
        customer, created = Customer.objects.get_or_create(admin=request.user)

        # Retrieve form data
        pan_card_number = request.POST.get('pan_number')
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        upload_image = request.FILES.get('upload_image')
        upload_sign = request.FILES.get('upload_sign')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount1)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
        # Perform basic form validation
         if not (pan_card_number and name and father_name and dob and gender and upload_image and upload_sign):
            return HttpResponseBadRequest("All fields are required")

        # Create and save PanManualPdf object
         pan_manual = PanManualPdf(
            customer_id=customer,
            pan_card_number=pan_card_number,
            name=name,
            father_name=father_name,
            dob=dob,
            gender=gender,
            upload_image=upload_image,
            upload_sign=upload_sign,
            order_id=order_id,
         )
         pan_manual.save()
         response_payment['name'] = name
         return render(request,'Customer/pancardmanualpdf.html', {'payment':response_payment})

    return redirect('pan_manual_pdf')
@csrf_exempt
def panmanualstatus(request):
    response=request.POST
    check={
    'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=PanManualPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/panmanualstatus.html',{'status':True})
    except:
        return render(request,'Sucess/panmanualstatus.html',{'status':False})
    
@login_required(login_url='/')
def find_pan_card(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/findpancard.html',{'amount':amount})
@login_required(login_url='/')
def FindPancardList(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = FindPanCard.objects.filter(customer_id=customer)  
    return render(request,'Customer/findpancardlist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def FindPannumbersave(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        aadhar_number=request.POST.get('aadhar_number')
        mobile_number=request.POST.get('mobile_no')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount2)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and aadhar_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=FindPanCard(
            customer_id=customer,
            name=name,
            aadhar_number=aadhar_number,
            mobile_number=mobile_number,
            order_id=order_id 
         )
         pan_data.save()
         response_payment['name'] = name
         
         return render(request,'Customer/findpancard.html',{'payment':response_payment})
    return render(request,'Customer/findpancard.html')
@csrf_exempt
def findpannumberstatus(request):
    response=request.POST
    check={
    'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=FindPanCard.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Customer/findpannumberpaymentstatus.html',{'status':True})
    except:
        return render(request,'Customer/findpannumberpaymentstatus.html',{'status':False})

@login_required(login_url='/')
def incomecertificate(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/incomecertificateapply.html',{'amount':amount})
@login_required(login_url='/')
def incomecertificatelist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    income_detail = IncomeCertificate.objects.filter(customer_id=customer)  
    return render(request,'Customer/incomecertificatelist.html',{'customer':income_detail})
@login_required(login_url='/')
def incomecertificatesave(request):
    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name=request.POST.get('name')
        samagr_id=request.POST.get('samagr_id')
        mobile_number=request.POST.get('mobile_no')
        upload_file = request.FILES.get('upload_file')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount3)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and samagr_id and mobile_number and upload_file):
            return HttpResponseBadRequest("All fields are required")
         income_detail=IncomeCertificate(
            customer_id=customer,
            name=name,
            samagr_id=samagr_id,
            mobile_number=mobile_number,
            upload_file=upload_file,
            order_id=order_id,
         )
         income_detail.save()
         response_payment['name'] = name
        return render(request,'Customer/incomecertificateapply.html',{'payment':response_payment})
    return render(request,'Customer/incomecertificateapply.html')
@csrf_exempt
def incomecertificatestatus(request):
    response=request.POST
    
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=IncomeCertificate.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/incomecertificatestatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/incomecertificatestatus.html',{'status':False})

@login_required(login_url='/')
def domicalcertificate(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/domicalcertificateapply.html',{'amount':amount})
@login_required(login_url='/')
def domicalcertificatelist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    income_detail = DomicalCertificate.objects.filter(customer_id=customer)  
    return render(request,'Customer/domicalcertificatelist.html',{'customer':income_detail})
@login_required(login_url='/')
def domicalcertificatesave(request):
    if request.method == 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name=request.POST.get('name')
        samagr_id=request.POST.get('samagr_id')
        mobile_number=request.POST.get('mobile_no')
        upload_file = request.FILES.get('upload_file')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount4)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and samagr_id and mobile_number and upload_file):
            return HttpResponseBadRequest("All fields are required")
         income_detail=DomicalCertificate(
            customer_id=customer,
            name=name,
            samagr_id=samagr_id,
            mobile_number=mobile_number,
            upload_file=upload_file,
            order_id=order_id
         )
         income_detail.save()
         response_payment['name'] = name
         return render(request,'Customer/domicalcertificateapply.html',{'payment':response_payment})
    return render(request,'Customer/domicalcertificateapply.html')
@csrf_exempt
def domicalcertificatestatus(request):
    response=request.POST
    
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=DomicalCertificate.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/domicalcertificatestatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/domicalcertificatestatus.html',{'status':False})

@login_required(login_url='/')
def pannumbertoaadhar(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/pannumbertoaadhar.html',{'amount':amount})
@login_required(login_url='/')
def FindAadharcardList(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = FindAadharCard.objects.filter(customer_id=customer)  
    return render(request,'Customer/findpantoaadhar.html',{'customer':find_pan_number})
@login_required(login_url='/')
def FindAadharnumbersave(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        pan_number=request.POST.get('pan_number')
        mobile_number=request.POST.get('mobile_number')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount5)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and pan_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=FindAadharCard(
            customer_id=customer,
            name=name,
            pan_number=pan_number,
            mobile_number=mobile_number, 
            order_id=order_id
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/pannumbertoaadhar.html',{'payment':response_payment})
    return render(request,'Customer/pannumbertoaadhar.html')
@csrf_exempt
def pantoaadharstatus(request):
    response=request.POST
    
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=FindAadharCard.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/pannumbertoaadharnumberstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/pannumbertoaadharnumberstatus.html',{'status':False})
@login_required(login_url='/')
def uidtopdf(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/uidtopdfapply.html',{'amount':amount})
@login_required(login_url='/')
def uidtopdflist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = UidToPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/uidtopdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def uidtopdfsave(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        aadhar_number=request.POST.get('aadhar_number')
        mobile_number=request.POST.get('mobile_number')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount6)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and aadhar_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=UidToPdf(
            customer_id=customer,
            name=name,
            aadhar_number=aadhar_number,
            mobile_number=mobile_number, 
            order_id=order_id
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/uidtopdfapply.html',{'payment':response_payment})
    return render(request,'Customer/uidtopdfapply.html')
@csrf_exempt
def uidtopdfstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=UidToPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/uidtopdfstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/uidtopdfstatus.html',{'status':False})
@login_required(login_url='/')
def eidtouid(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/eidtouidapply.html',{'amount':amount})
@login_required(login_url='/')
def eidtouidlist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = EidtoUid.objects.filter(customer_id=customer)  
    return render(request,'Customer/eidtouidlist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def eidtouidsave(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        eid=request.POST.get('eid')
        mobile_number=request.POST.get('mobile_number')
        date=request.POST.get('date')
        time=request.POST.get('time')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount7)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and eid and date and time and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=EidtoUid(
            customer_id=customer,
            name=name,
            eid=eid,
            date=date,
            time=time,
            mobile_number=mobile_number,
            order_id=order_id 
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/eidtouidapply.html',{'payment':response_payment})
    return render(request,'Customer/eidtouidapply.html')
@csrf_exempt
def eidtouidstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=EidtoUid.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/eidtouidstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/eidtouidstatus.html',{'status':False})
@login_required(login_url='/')
def matchingaadharcardduplicatetopdf(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/matchingaadharcardduplicatetopdf.html',{'amount':amount})
@login_required(login_url='/')
def matchingaadharcardduplicatetopdflist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = MatchAadharCardToPDf.objects.filter(customer_id=customer)  
    return render(request,'Customer/matchingaadharcardduplicatetopdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def matchaadharcardtopdfsave(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        eid=request.POST.get('eid')
        mobile_number=request.POST.get('mobile_number')
        date=request.POST.get('date')
        time = request.POST.get('timehya') 
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount8)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and eid and date and time and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=MatchAadharCardToPDf(
            customer_id=customer,
            name=name,
            eid=eid,
            date=date,
            time=time,
            mobile_number=mobile_number, 
            order_id=order_id
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/matchingaadharcardduplicatetopdf.html',{'payment':response_payment})
    return render(request,'Customer/matchingaadharcardduplicatetopdf.html')
@csrf_exempt
def matchingaadhartopdftatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=MatchAadharCardToPDf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/matchaadharcardpdfstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/matchaadharcardpdfstatus.html',{'status':False})
@login_required(login_url='/')
def matchingaadharcardduplicatetonumber(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/matchingaadharcardduplicatetonumber.html',{'amount':amount})
@login_required(login_url='/')
def matchingaadharcardduplicatetonumberlist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = MatchAadharNumber.objects.filter(customer_id=customer)  
    return render(request,'Customer/matchingaadharcardduplicatetonumberlist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def matchaadharcardtonumbersave(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        eid=request.POST.get('eid')
        mobile_number=request.POST.get('mobile_number')
        date=request.POST.get('date')
        dob = request.POST.get('date_of_birth')
        pin_code=request.POST.get('pin')
        time=request.POST.get('time')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount9)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and eid and date and time and dob and pin_code and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=MatchAadharNumber(
            customer_id=customer,
            name=name,
            eid=eid,
            date=date,
            dob=dob,
            pin_code=pin_code,
            time=time,
            mobile_number=mobile_number, 
            order_id=order_id
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/matchingaadharcardduplicatetonumber.html',{'payment':response_payment})
    return render(request,'Customer/matchingaadharcardduplicatetonumber.html')
@csrf_exempt
def matchingaadhartonumbertatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=MatchAadharNumber.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/matchaadharcardnumberstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/matchaadharcardnumberstatus.html',{'status':False})
@login_required(login_url='/')
def detailstopdf(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/detailstopdfapply.html',{'amount':amount})
@login_required(login_url='/')
def detailstopdflist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = DetailsToPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/detailstopdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def details_to_pdf_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        select_guardian=request.POST.get('select_guardian')
        guardian_name=request.POST.get('guardian_name')
        state=request.POST.get('state')
        distric=request.POST.get('distric')
        address=request.POST.get('address')
        pin_code=request.POST.get('pin_code')                 
    
        mobile_number=request.POST.get('mobile_number')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount10)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and dob and gender and select_guardian and guardian_name and pin_code and mobile_number and state and distric and address):
            return HttpResponseBadRequest("All fields are required")
         pan_data=DetailsToPdf(
            customer_id=customer,
            name=name,
            dob=dob,
            gender=gender,
            select_guardian=select_guardian,
            guardian_name=guardian_name,
            pin_code=pin_code,
            state=state,
            distric=distric,
            address=address,
            mobile_number=mobile_number, 
            order_id=order_id,
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/detailstopdfapply.html',{'payment':response_payment})
    return render(request,'Customer/detailstopdfapply.html')
@csrf_exempt
def detailtopdfstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=DetailsToPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/detailtopdfstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/detailtopdfstatus.html',{'status':False})
@login_required(login_url='/')
def rashannumberapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/rashannumberapply.html',{'amount':amount})
@login_required(login_url='/')
def rashannumberlist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = RashanNumbertoUid.objects.filter(customer_id=customer)  
    return render(request,'Customer/rashannumberlist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def rashan_number_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        rashan_number=request.POST.get('rashan_number')
        mobile_number=request.POST.get('mobile_number')
        
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount11)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and rashan_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=RashanNumbertoUid(
            customer_id=customer,
            name=name,
            rashan_number=rashan_number,
            mobile_number=mobile_number, 
            order_id=order_id,
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/rashannumberapply.html',{'payment':response_payment})
    return render(request,'Customer/rashannumberapply.html')
@csrf_exempt
def rashannumbertatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=RashanNumbertoUid.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/rashannumberstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/rashannumberstatus.html',{'status':False})
@login_required(login_url='/')
def pmkishanregistrationnumberapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/pmkishanregistrationapply.html',{'amount':amount})
@login_required(login_url='/')
def pmkishanregistrationnumberlist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = PMKishanRegistrationNumber.objects.filter(customer_id=customer)  
    return render(request,'Customer/pmkishanregistrationumberlist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def pm_kishan_registration_number_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        aadhar_number=request.POST.get('aadhar_number')
        mobile_number=request.POST.get('mobile_number')
        
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount12)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not ( aadhar_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=PMKishanRegistrationNumber(
            customer_id=customer,
           aadhar_number=aadhar_number,
            mobile_number=mobile_number, 
            order_id=order_id,
         )
         pan_data.save()
          
        return render(request,'Customer/pmkishanregistrationapply.html',{'payment':response_payment})
    return render(request,'Customer/pmkishanregistrationapply.html')
@csrf_exempt
def pmkishanregistrationtatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    client=razorpay.Client(auth=('rzp_test_pwchuxr8hCkkZZ','qlrmhVqbMEZxsAVNfxdlpQRS'))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=PMKishanRegistrationNumber.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/pmkishanregistrationstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/pmkishanregistrationstatus.html',{'status':False})
@login_required(login_url='/')
def dlpdfapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/dlpdfapply.html',{'amount':amount})
@login_required(login_url='/')
def dl_pdf_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name=request.POST.get('name')
        dl_number=request.POST.get('dl_number')
        dob=request.POST.get('dob')
        mobile_number=request.POST.get('mobile_number')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount13)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
        
         if not ( name and dob  and dl_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=DLPdf(
            customer_id=customer,
          name=name,
          dl_number=dl_number,
          dob=dob,
         mobile_number=mobile_number, 
         order_id=order_id,
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/dlpdfapply.html',{'payment':response_payment})
    return render(request,'Customer/dlpdfapply.html')
@csrf_exempt
def dlpdfstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=DLPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/dlpdfstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/dlpdfstatus.html',{'status':False})
@login_required(login_url='/')
def dlpdflist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = DLPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/dlpdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def finddlnumberapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/finddlnumberapply.html',{'amount':amount})
@login_required(login_url='/')
def finddlnumberlist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = FindDlNumber.objects.filter(customer_id=customer)  
    return render(request,'Customer/finddlnumberlist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def find_dl_number_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name=request.POST.get('name')
        dob=request.POST.get('dob')
        state=request.POST.get('state')
        mobile_number=request.POST.get('mobile_number')
        father_name=request.POST.get('father_name')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount14)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not ( name and dob  and state and father_name and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=FindDlNumber(
            customer_id=customer,
            father_name=father_name,
          name=name,
          state=state,
          dob=dob,
         mobile_number=mobile_number,
         order_id=order_id, 
         )
         pan_data.save()
         response_payment['name'] = name
         return render(request,'Customer/finddlnumberapply.html',{'payment':response_payment})
    return render(request,'Customer/finddlnumberapply.html')
@csrf_exempt
def dlnumberstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=FindDlNumber.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/dlnumberstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/dlnumberstatus.html',{'status':False})
@login_required(login_url='/')
def ayushmancardpdfapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/ayushmancardpdfapply.html',{'amount':amount})
@login_required(login_url='/')
def findayushmancardpdflist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number = FindAyushmanCardPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/findayushmancardpdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def find_ayushmancard_pdf_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
       
        select_profe=request.POST.get('select_profe')
        state=request.POST.get('state')
        mobile_number=request.POST.get('mobile_number')
        enter_details=request.POST.get('enter_details')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount15)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (  select_profe  and state and enter_details and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=FindAyushmanCardPdf(
            customer_id=customer,
            select_profe=select_profe,
          state=state,
          enter_details=enter_details,
         mobile_number=mobile_number, 
         order_id=order_id,
         )
         pan_data.save()
        
        return render(request,'Customer/ayushmancardpdfapply.html',{'payment':response_payment})
    return render(request,'Customer/ayushmancardpdfapply.html')
@csrf_exempt
def ayushmancardstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=FindAyushmanCardPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/ayushmancardstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/ayushmancardstatus.html',{'status':False})
@login_required(login_url='/')
def pmkishanregistpaymentapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/pmkishanregistpaymentapply.html',{'amount':amount})
@login_required(login_url='/')
def findpmkishanpaymentdetaillist(request):
    #  # Get the Customer object associated wthe logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number =FindPmKishanPaymentDetails.objects.filter(customer_id=customer)  
    return render(request,'Customer/findpmkishanpaymentdetaillist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def find_pm_kishan_payment_details_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
       
        aadhar_number=request.POST.get('aadhar_number')
        pm_kishan_id=request.POST.get('pm_kishan_id')
        mobile_number=request.POST.get('mobile_number')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount16)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not ( pm_kishan_id and aadhar_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=FindPmKishanPaymentDetails(
            customer_id=customer,
           pm_kishan_id=pm_kishan_id,
           aadhar_number=aadhar_number,
         mobile_number=mobile_number, 
         order_id=order_id
         )
         pan_data.save()
        
        return render(request,'Customer/pmkishanregistpaymentapply.html',{'payment':response_payment})
    return render(request,'Customer/pmkishanregistpaymentapply.html')
@csrf_exempt
def pmkishapaymentstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=FindPmKishanPaymentDetails.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/pmkishapaymentstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/pmkishapaymentstatus.html',{'status':False})
@login_required(login_url='/')
def rcpdfapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/rcpdfapply.html',{'amount':amount})
@login_required(login_url='/')
def rcpdflist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number =FindRcPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/findrcpdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def rc_pdf_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
       
        rc_number=request.POST.get('rc_number')
        mobile_number=request.POST.get('mobile_number')
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount17)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (rc_number and mobile_number):
            return HttpResponseBadRequest("All fields are required")
         pan_data=FindRcPdf(
            customer_id=customer,
           rc_number=rc_number,
            mobile_number=mobile_number, 
            order_id=order_id,
         )
         pan_data.save()
        
        return render(request,'Customer/rcpdfapply.html',{'payment':response_payment})
    return render(request,'Customer/rcpdfapply.html')
@csrf_exempt
def rcpdfstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=FindRcPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/rcpdfstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/rcpdfstatus.html',{'status':False})
@login_required(login_url='/')
def jobcardpdfapply(request):
    amount=AmountSet.objects.first()
    return render(request,'Customer/jobcardapply.html',{'amount':amount})
@login_required(login_url='/')
def jobcardpdfist(request):
    #  # Get the Customer object associated with the logged-in user
    customer = request.user.customer_profile
    
    # # Filter PanManualPdf objects based on the associated Customer object
    find_pan_number =JobCardPdf.objects.filter(customer_id=customer)  
    return render(request,'Customer/jobcardpdflist.html',{'customer':find_pan_number})
@login_required(login_url='/')
def jobcard_to_pdf_save(request):
    if request.method== 'POST':
        customer, created = Customer.objects.get_or_create(admin=request.user)
        name= request.POST.get('name')
        father_name=request.POST.get('father_name')
        state=request.POST.get('state')
        distric=request.POST.get('distric')
        block=request.POST.get('block')
        village=request.POST.get('village')
        dob=request.POST.get('dob')
        mobile_number=request.POST.get('mobile_number')
        
        amount=AmountSet.objects.first()
        key=SetKeys.objects.first()
        client=razorpay.Client(auth=(key.key_id,key.secret_key))
        response_payment =client.order.create(dict(amount=int(amount.amount18)*100,
                                                   currency='INR')
                                              )
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status == 'created':
         if not (name and dob and father_name and block and state and distric and mobile_number and village):
            return HttpResponseBadRequest("All fields are required")
         pan_data=JobCardPdf(
            customer_id=customer,
            name=name,
            dob=dob,
            father_name=father_name,
            block=block,
            state=state,
            distric=distric,
            village=village,
            mobile_number=mobile_number,
          order_id=order_id,
         )
         pan_data.save()
        
        return render(request,'Customer/jobcardapply.html',{'payment':response_payment})
    return render(request,'Customer/jobcardapply.html')
@csrf_exempt
def jobcardpdfstatus(request):
    response=request.POST
    check={
   'razorpay_order_id': response['razorpay_order_id'],
   'razorpay_payment_id': response['razorpay_payment_id'],
   'razorpay_signature': response['razorpay_signature']
    }
    key=SetKeys.objects.first()
    client=razorpay.Client(auth=(key.key_id,key.secret_key))
    try :
        client.utility.verify_payment_signature(check)
        cold_cofee=JobCardPdf.objects.get(order_id=response['razorpay_order_id'])
        cold_cofee.payment_id=response['razorpay_payment_id']
        cold_cofee.paid=True 
        cold_cofee.save()
        return render(request,'Sucess/jobcardpdfstatus.html',{'status':True})
    except Exception as e:
        print(e)
        return render(request,'Sucess/jobcardpdfstatus.html',{'status':False})
def register_customer(request):
    if request.method == 'POST':
       
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
       
       
        password=request.POST.get('password')
        print(first_name,last_name,email,username,password)
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
               
            )
            customer.save()
            messages.success(request,user.first_name+" " + user.last_name +" Sucessfully added")
            return redirect('do_login')
            
          
    return render(request, 'Admin/customer_register.html')