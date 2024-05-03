from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class CustomUser(AbstractUser):
    USER_TYPES = (
        (1, 'Admin'),
        (2, 'Customer'),
    )
    user_type = models.IntegerField(choices=USER_TYPES, default=1)
    profile_pic = models.ImageField(upload_to="media/profile_pic")
class Customer(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    def __str__(self) :
        return self.admin.first_name
class PanManualPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pan_card_number = models.CharField(max_length=12)
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    upload_image = models.ImageField(upload_to="media/PanManualPdf")
    upload_sign = models.ImageField(upload_to="media/PanManualPdf")
    upload_file = models.FileField(upload_to='media/PanManualPdf')
    status=models.IntegerField(default=0)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name
class FindPanCard(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    aadhar_number = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    status=models.IntegerField(default=0)
    pan_number=models.CharField(max_length=12)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def __str__(self) :
        return self.customer_id.admin.first_name
class IncomeCertificate(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    samagr_id=models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    upload_file=models.ImageField(upload_to='media/Incomecertificate')
    download_file=models.ImageField(upload_to='media/Incomecertificate')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name
class DomicalCertificate(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    samagr_id=models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/Domicalcertificate')
    download_file=models.ImageField(upload_to='media/Domicalcertificate')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name
class FindAadharCard(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    aadhar_number = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    pan_number=models.CharField(max_length=12)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name    
class UidToPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    aadhar_number = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/UidToPdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name 
class EidtoUid(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    eid = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    date=models.DateField()
    time=models.CharField(max_length=50)
    uid=models.CharField(max_length=12)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name    
     
class MatchAadharCardToPDf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    eid = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    date=models.DateField()
    time=models.CharField(max_length=50)
    upload_file=models.ImageField(upload_to='media/MatchAadharcardpdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def __str__(self) :
        return self.customer_id.admin.first_name    
class MatchAadharNumber(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    eid = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    date=models.DateField()
    dob = models.DateField()
    time=models.CharField(max_length=50)
    pin_code=models.CharField(max_length=10)
    upload_number=models.CharField(max_length=20)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name
class RashanNumbertoUid(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    rashan_number = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    uid=models.CharField(max_length=20)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name    
class PMKishanRegistrationNumber(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    kishan_registration_number=models.CharField(max_length=20)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name 
class DLPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    dl_number = models.CharField(max_length=12)
    dob=models.DateField()
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/DlPdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name            
class FindDlNumber(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    father_name = models.CharField(max_length=50)
    dob=models.DateField()
    state = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    upload_dl_number=models.CharField(max_length=20)
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name            
class FindAyushmanCardPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    select_profe= models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    state = models.CharField(max_length=12)
    enter_details = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=12)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/AyushmanCardpdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name            
class FindPmKishanPaymentDetails(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    aadhar_number= models.CharField(max_length=20)
    pm_kishan_id = models.CharField(max_length=20)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=20)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/PmKishanPaymentDetails')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name      
class FindRcPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rc_number= models.CharField(max_length=20)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    mobile_number = models.CharField(max_length=20)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/RcPdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name   
class DetailsToPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    dob=models.DateField()
    gender=models.CharField(max_length=50)
    select_guardian=models.CharField(max_length=50)
    guardian_name=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    distric=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    pin_code=models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=20)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/Detailstopdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)

    def _str_(self) :
        return self.customer_id.admin.first_name      
class JobCardPdf(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name= models.CharField(max_length=50)
    prev_date = models.DateField(null=True, default=None)
    is_valid=models.BooleanField(null=True,default=None)
    father_name= models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    distric=models.CharField(max_length=50)
    block=models.CharField(max_length=50)
    village=models.CharField(max_length=50)
    dob=models.DateField()
    mobile_number = models.CharField(max_length=20)
    status=models.IntegerField(default=0)
    upload_file=models.ImageField(upload_to='media/Detailstopdf')
    order_id=models.CharField(max_length=100,blank=True)
    payment_id=models.CharField(max_length=100,blank=True)
    paid=models.BooleanField(default=False,blank=True)
    def _str_(self) :
        return self.customer_id.admin.first_name    
class SetKeys(models.Model):
    key_id=models.CharField(max_length=100)
    secret_key=models.CharField(max_length=100) 
class AmountSet(models.Model):
    amount1=models.CharField(max_length=10,blank=True)
    amount2=models.CharField(max_length=10,blank=True)                       
    amount3=models.CharField(max_length=10,blank=True)
    amount4=models.CharField(max_length=10,blank=True)
    amount5=models.CharField(max_length=10,blank=True)
    amount6=models.CharField(max_length=10,blank=True)
    amount7=models.CharField(max_length=10,blank=True)
    amount8=models.CharField(max_length=10,blank=True)
    amount9=models.CharField(max_length=10,blank=True)
    amount10=models.CharField(max_length=10,blank=True)
    amount11=models.CharField(max_length=10,blank=True)
    amount12=models.CharField(max_length=10,blank=True)
    amount13=models.CharField(max_length=10,blank=True)
    amount14=models.CharField(max_length=10,blank=True)
    amount15=models.CharField(max_length=10,blank=True)
    amount16=models.CharField(max_length=10,blank=True)
    amount17=models.CharField(max_length=10,blank=True)
    amount18=models.CharField(max_length=10,blank=True)
    amount19=models.CharField(max_length=10,blank=True)
    amount20=models.CharField(max_length=10,blank=True)
    amount21=models.CharField(max_length=10,blank=True)
    amount22=models.CharField(max_length=10,blank=True)
    amount23=models.CharField(max_length=10,blank=True)
    amount24=models.CharField(max_length=10,blank=True)
    amount25=models.CharField(max_length=10,blank=True)
    amount26=models.CharField(max_length=10,blank=True)
    amount27=models.CharField(max_length=10,blank=True)
    amount28=models.CharField(max_length=10,blank=True)
    amount29=models.CharField(max_length=10,blank=True)
    amount30=models.CharField(max_length=10,blank=True)
class Help(models.Model):
      customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
      name=models.CharField(max_length=100)
      email=models.EmailField(max_length=254)
      mobile_no=models.CharField(max_length=20)
      description =models.CharField(max_length=254)    
class contactus(models.Model):
      customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
      name=models.CharField(max_length=100)
      email=models.EmailField(max_length=254)
      description =models.CharField(max_length=254)       
    
          
                                