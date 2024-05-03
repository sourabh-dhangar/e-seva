from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(PanManualPdf)
admin.site.register(FindPanCard)
admin.site.register(IncomeCertificate)
admin.site.register(DomicalCertificate)
admin.site.register(FindAadharCard)
admin.site.register(UidToPdf)
admin.site.register(EidtoUid)
admin.site.register(MatchAadharCardToPDf)
admin.site.register(MatchAadharNumber)
admin.site.register(RashanNumbertoUid)
admin.site.register(PMKishanRegistrationNumber)
admin.site.register(DLPdf)
admin.site.register(FindDlNumber)
admin.site.register(FindAyushmanCardPdf)
admin.site.register(FindPmKishanPaymentDetails)
admin.site.register(FindRcPdf)
admin.site.register(DetailsToPdf)
admin.site.register(JobCardPdf)
admin.site.register(SetKeys)
admin.site.register(AmountSet)
admin.site.register(Help)
admin.site.register(contactus)