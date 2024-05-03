"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views,adminviews,customerviews
urlpatterns = [
    path('admin/', admin.site.urls),
    # LOGIN PATH
    path('',views.LOGIN,name='login'),
    path('do_login',views.do_login,name='do_login'),
    path('do_logout/',views.do_logout,name='do_logout'),
    # PROFILE UPDATE
    path('profile/',views.profile,name='profile'),
    path('profile/update/',views.profile_update,name='profile_update'),
    # ADMIN PATH
    path('home/',adminviews.home,name='admin_home'),
    path('add/customer/', adminviews.add_customer, name='add_customer'),
    path('allcustomer/',adminviews.view_all_customer,name='view_all_customer'),
    path('customer/edit/<str:id>/', adminviews.edit_customer, name='edit_customer'),
    path('customer/update/',adminviews.update_customer,name='update_customer'),
    path('customer/delete/<str:id>/',adminviews.customer_delete,name='customer_delete'),
    # ADMIN PATH FOR FIND PAN CARD NUMBER
    path('all/pan/list',adminviews.view_all_pan_number_list,name='all_pan_number_list'),
    path('pan/number/delete/<str:id>/',adminviews.pan_number_delete,name='pan_number_delete'),
    path('edit/pan/number/<str:id>/',adminviews.edit_pan_number,name='edit_pan_number'),
    path('pan/number/update/',adminviews.update_pan_number,name='update_pan_number'),
    # ADMIN PATH FOR PAN CARD MANUAL PDF
    path('all_pan_manual_pdf/',adminviews.view_all_pan_manual,name='all_pan_manual'),
    path('edit/pan_manual_pdf/<str:id>/',adminviews.edit_pan_manual_pdf,name='edit_pan_manual_pdf'),
    path('pan_manual/update/',adminviews.update_pan_manual_pdf,name='update_pan_manual_pdf'),
    path('pan_manual/delete/<str:id>/',adminviews.pan_manual_delete,name='pan_manual_delete'),
    # ADMIN PATH FOR INCOME CERTIFICATE DOWNLOAD
    path('all/income/detail/',adminviews.view_all_income_list,name='all_income_detail'),
    path('income/delete/<str:id>/',adminviews.income_certificate_delete,name='income_certificate_delete'),
    path('edit/income/detail/<str:id>/',adminviews.edit_income_certificate,name='income_certificate_detail'),
    path('income/detail/update/',adminviews.update_income_detail,name='update_income_detail'),
    # ADMIN PATH FOR DOMICAL CERTIFICATE
    path('all/domical/detail/',adminviews.view_all_domical_list,name='all_domical_detail'),
    path('domical/delete/<str:id>/',adminviews.domical_certificate_delete,name='domical_certificate_delete'),
    path('edit/domical/detail/<str:id>/',adminviews.edit_domical_certificate,name='domical_certificate_detail'),
    path('domical/detail/update/',adminviews.update_domical_detail,name='update_domical_detail'),
    # ADMIN PATH FOR PAN NUMBER TO AADHAR NUMBER 
    path('pannumber/details/',adminviews.view_all_aadhar_number_list,name='all_aadhar_manual'),
    path('edit/aadhar/number/<str:id>/',adminviews.edit_aadhar_number,name='edit_aadhar_number'),
    path('pan/aadhar/number/update/',adminviews.update_aadhar_number,name='update_aadhar_number'),
    path('aadhar/number/delete/<str:id>/',adminviews.aadhar_number_delete,name='aadhar_number_delete'),
    # ADMIN PATH FOR UID TO PDF 
    path('uid/details/',adminviews.view_all_uid_list,name='all_uid_list'),
    path('uid/delete/<str:id>/',adminviews.uid_pdf_delete,name='uid_pdf_delete'),
    path('edit/uid/pdf/<str:id>/',adminviews.edit_uid_pdf,name='edit_uid_to_pdf'),
    path('uid/pdf/update/',adminviews.update_uid_to_pdf,name='update_uid_to_pdf'),
    # ADMIN PATH FOR EID TO UID 
    path('eid/details/',adminviews.view_all_eid_list,name='all_eid_list'),
    path('eid/delete/<str:id>/',adminviews.eid_to_uid_delete,name='eid_to_uid_delete'),
    path('edit/eid/uid/<str:id>/',adminviews.edit_eid_to_uid,name='edit_eid_to_uid'),
    path('eid/to/uid/update/',adminviews.update_eid_to_uid,name='update_eid_to_uid'),
    # ADMIN PATH FOR MATCHING AADHAR CARD TO PDF
    path('matching/aadhar/list/',adminviews.view_all_matching_aadhar_list,name='view_all_matching_aadhar_list'),
    path('matching/aadhar/delete/<str:id>/',adminviews.matching_aadhar_pdf_delete,name='matching_aadhar_pdf_delete'),
    path('edit/matching/aadhar/pdf/<str:id>/',adminviews.edit_matching_aadhar_duplicate,name='edit_matching_aadhar_duplicate'),
    path('matcing/aadhar/pdf/update/',adminviews.matching_aadhar_to_pdf_save,name='matching_aadhar_to_pdf_save'),
    # ADMIN PATH FOR MATCHING AADHAR CARD TO NUMBER 
    path('matching/aadhar/number/admin/list/',adminviews.view_all_matching_aadhar_number_list,name='view_all_matching_aadhar_number_list'),
    path('matching/aadhar/number/delete/<str:id>/',adminviews.matching_aadhar_number_delete,name='matching_aadhar_number_delete'),
    path('edit/matching/aadhar/number/<str:id>/',adminviews.edit_matching_aadhar_duplicate_number,name='edit_matching_aadhar_duplicate_number'),
    path('matcing/aadhar/number/update/',adminviews.matching_aadhar_to_number_save,name='matching_aadhar_to_number_save'),
    # ADMIN PATH FOR DETAILS TO PDF
    path('details/pdf/admin/list/',adminviews.view_all_details_to_list,name='view_all_details_to_list'),
    path('details/pdf/delete/<str:id>/',adminviews.details_pdf_delete,name='details_pdf_delete'),
     path('edit/details/pdf/<str:id>/',adminviews.edit_details_pdf,name='edit_details_pdf'),
     path('details/pdf/update/',adminviews.details_pdf_update,name='details_pdf_update'),
    # ADMIN PATH FOR RASHAN NUMBER TO UID
    path('rashan/number/details/',adminviews.view_all_rashan_list,name='view_all_rashan_list'),
    path('rashan/number/delete/<str:id>/',adminviews.eid_to_rashan_delete,name='eid_to_rashan_delete'),
    path('edit/rashan/number/uid/<str:id>/',adminviews.edit_rashan_number_uid,name='edit_rashan_number_uid'),
    path('rashan/number/update/',adminviews.rashan_number_update,name='rashan_number_update'),
    # ADMIN PATH FOR PM KISHAN REGISTRATION NUMBER 
    
    path('pm/kishan/registration/number/details/',adminviews.view_all_pm_kishan_registration_list,name='view_all_pm_kishan_registration_list'),
    path('pm/kishan/registration/number/delete/<str:id>/',adminviews.pm_kishan_registration_number_delete,name='pm_kishan_registration_number_delete'),
    path('eidt/pm/kishan/registration/<str:id>/',adminviews.edit_pm_kishan_registration_number,name='edit_pm_kishan_registration_number'),
    path('pm/kishan/registration/number/update/',adminviews.pm_kishan_registration_update,name='pm_kishan_registration_update'),
    # ADMIN PATH FOR DL TO PDF
    path('dl/pdf/admin/details/',adminviews.view_all_dl_pdf_list,name='view_all_dl_pdf_list'),
    path('dl/pdf/delete/<str:id>/',adminviews.dl_pdf_delete,name='dl_pdf_delete'),
    path('edit/dl/pdf/<str:id>/',adminviews.edit_dl_pdf,name='edit_dl_pdf'),
    path('dl/pdf/update/',adminviews.dl_pdf_update,name='dl_pdf_update'),
    # ADMIN PATH FOR DOWNLOAD AYUSHMAN CARD
    path('ayushman/card/download/details/',adminviews.view_all_ayushman_card_download_list,name='view_all_ayushman_card_download_list'),
    path('find/ayushmancard/delete/<str:id>/',adminviews.find_ayushman_card_delete,name='find_ayushman_card_delete'),
    path('edit/ayushman/card/download/<str:id>/',adminviews.edit_ayushman_card_download,name='edit_ayushman_card_download'),
     path('ayushman/card/download/update/',adminviews.ayushman_card_download_update,name='ayushman_card_download_update'),
    #  ADMIN PATH FOR PM KISHAN PAYMENT DETAILS 
    path('pm/kishan/payment/details/',adminviews.view_all_pm_kishan_payment_details,name='view_all_pm_kishan_payment_details'),
    path('pm/kishan/payment/delete/<str:id>/',adminviews.find_pm_kishan_payment_delete,name='find_pm_kishan_payment_delete'),
    path('edit/pm/kishan/payment/<str:id>/',adminviews.edit_pm_kishan_payment_details,name='edit_pm_kishan_payment_details'),
    path('pm/kishan/payment/update/',adminviews.pm_kishan_payment_update,name='pm_kishan_payment_update'),
    # ADMIN PATH FOR RC PDF 
    path('rc/pdf/details/',adminviews.view_all_rc_pdf_list,name='view_all_rc_pdf_list'),
    path('rc/pdf/delete/<str:id>/',adminviews.rc_pdf_delete,name='rc_pdf_delete'),
    path('edit/rc/pdf/<str:id>/',adminviews.edit_rc_pdf_details,name='edit_rc_pdf_details'),
    path('rc/pdf/update/',adminviews.rc_pdf_update,name='rc_pdf_update'),
    # CUSTOMER PATH FOR REGISTER 
    path('customer/register',customerviews.register_customer,name='register_customer'),
   
    # CUSTOMER PATH FOR FIND DL NUMBER
    path('find/dl/number/details/',adminviews.view_all_find_dl_number_list,name='view_all_find_dl_number_list'),  
    path('find/dl/number/delete/<str:id>/',adminviews.find_dl_number_delete,name='find_dl_number_delete'),
    path('eidt/find/dl/number/<str:id>/',adminviews.edit_find_dl_number,name='edit_find_dl_number'),
    path('find/dl/number/update/',adminviews.find_dl_number_update,name='find_dl_number_update'),
    #  ADMIN PATH FOR JOBCARD TO PDF
    path('job/card/pdf/details/',adminviews.view_all_job_card_pdf_list,name='view_all_job_card_pdf_list'),
    path('job/card/pdf/delete/<str:id>/',adminviews.job_card_pdf_delete,name='job_card_pdf_delete'),  
    path('eidt/job/card/pdf/<str:id>/',adminviews.edit_job_card_pdf,name='edit_job_card_pdf'),
    path('job/card/pdf/update/',adminviews.jobcard_pdf_update,name='jobcard_pdf_update'),
    # IMPORTANT PATH FOR ADMIN 
    path('set/key',adminviews.set_key,name='set_key'),
    path('edit/key/',adminviews.edit_key,name='edit_key'),
    path('update/key',adminviews.edit_key_update,name='update_key'),
    path('help/list',adminviews.view_all_help,name='view_all_help'),
    path('help/delete/<str:id>/',adminviews.help_delete,name='help_delete'),  
    path('contactus/list',adminviews.view_all_contact,name='view_all_contact'),
    path('contact/delete/<str:id>/',adminviews.contactus_delete,name='contactus_delete'),
    
    #CUSTOMER PATH
    path('customer/home',customerviews.home,name='customer_home'),
    # CUSTOMER PATH FOR FIND PAN CARD NUMBER
    path('pan/number/apply/',customerviews.find_pan_card,name='find_pan_card'),
    path('pan/number/customer/list/',customerviews.FindPancardList,name='find_pan_card_list'),
    path('pan/number/save/',customerviews.FindPannumbersave,name="pan_number_save"),
    path('find/pan/number/status',customerviews.findpannumberstatus,name='findpannumberstatus'),
    # CUSTOMER PATH FOR   CARD MANUAL PDF 
    path('pan_manual_pdf/apply/',customerviews.PanCardManualPdf,name='pan_manual_pdf'),
    path('pan_manual_pdf/save/',customerviews.PanCardManualPdfsave,name="pan_manual_pdf_save"),
    path('pan_manual/customer/list/',customerviews.PanCardManualPdflist,name='pan_manual_pdf_list'),
    path('pan/manual/status/',customerviews.panmanualstatus,name='pan_manual_status'),
    # CUSTOMER PATH FOR INCOME CERTIFICATE
    path('income/apply',customerviews.incomecertificate,name='income_certificate'), 
    path('income/certificate/list',customerviews.incomecertificatelist,name="incomecertificatelist"),
    path('income/details/save/',customerviews.incomecertificatesave,name="income_certificate_save"),
    path('income/certificate/status/',customerviews.incomecertificatestatus,name='incomecertificatestatus'),
    # CUSTOMER PATH FOR DOMICAL CERTIFICATE 
    path('domical/apply',customerviews.domicalcertificate,name='domical_certificate'),
    path('domical/certificate/list',customerviews.domicalcertificatelist,name="domicalcertificatelist"),
    path('domical/details/save/',customerviews.domicalcertificatesave,name="domical_certificate_save"),
    path('domical/certificate/status/',customerviews.domicalcertificatestatus,name='domicalcertificatestatus'),
    # CUSTOMER PATH FOR PAN NUMBER TO AADHAR NUMBER
    path('pannumbertoaadhar/apply',customerviews.pannumbertoaadhar,name='pannumbertoaadhar'),
    path('pan/aadhar/list/',customerviews.FindAadharcardList,name='pantoaadharlist'),
    path('pan/aadhar/save/',customerviews.FindAadharnumbersave,name="pantoaadharsave"),
    path('pan/to/aadhar/status/',customerviews.pantoaadharstatus,name='pantoaadharstatus'),
    # CUSTOMER PATH FOR UID TO PDF
    path('uidtopdf/apply',customerviews.uidtopdf,name='uidtopdf'),
    path('uid/pdf/list/',customerviews.uidtopdflist,name='uidtopdflist'),
    path('uid/details/save/',customerviews.uidtopdfsave,name="uidtopdfsave"),
    path('uid/to/pdf/status',customerviews.uidtopdfstatus,name='uidtopdfstatus'),
    # CUSTOMER PATH FOR EID TO UID
    path('eidto/uid/apply',customerviews.eidtouid,name='eidtouid'),
    path('eidto/uid/list/',customerviews.eidtouidlist,name='eidtouidlist'),
    path('eid/uid/details/save/',customerviews.eidtouidsave,name="eidtouidsave"),
    path('eid/to/uid/status/',customerviews.eidtouidstatus,name='eidtouidstatus'),
    # CUSTOMER PATH FOR MATCHING AADHAR CARD TO PDF
    path('matching/aadhar/pdf/apply',customerviews.matchingaadharcardduplicatetopdf,name='matchingaadharcardduplicatetopdf'),
    path('matching/aadhar/pdf/list/',customerviews.matchingaadharcardduplicatetopdflist,name='matchingaadharcardduplicatetopdflist'),
    path('match/aadhar/duplicate/save/',customerviews.matchaadharcardtopdfsave,name="matchaadharcardtopdfsave"),
    path('match/aadhar/to/pdf/status/',customerviews.matchingaadhartopdftatus,name='matchingaadhartopdftatus'),
    # CUSTOMER VIEW FOR MATCHING AADHAR CARD TO NUMBER
    path('matching/aadhar/number/apply',customerviews.matchingaadharcardduplicatetonumber,name='matchingaadharcardduplicatetonumber'),
    path('matching/aadhar/number/list/',customerviews.matchingaadharcardduplicatetonumberlist,name='matchingaadharcardduplicatetonumberlist'),
    path('match/aadhar/duplicate/number/save/',customerviews.matchaadharcardtonumbersave,name="matchaadharcardtonumbersave"),
    path('match/aadhar/to/number/status',customerviews.matchingaadhartonumbertatus,name='matchingaadhartonumbertatus'),
    # CUSTOMER VIEW FOR DETAIS TO PDF
    path('detailstopdf/apply',customerviews.detailstopdf,name='detailstopdf'),
    path('details/pdf/list/',customerviews.detailstopdflist,name='detailstopdflist'),
    path('details/pdf/save/',customerviews.details_to_pdf_save,name="details_to_pdf_save"),
    path('detail/to/pdf/sucess/',customerviews.detailtopdfstatus,name='detailtopdfstatus'), 
    # CUSTOMER VIEW FOR RASHAN NUMBER TO UID
    path('rashannumber/uid/apply',customerviews.rashannumberapply,name='rashannumberapply'),
    path('rashannumber/uid/list/',customerviews.rashannumberlist,name='rashannumberlist'),
    path('rashan/number/save/',customerviews.rashan_number_save,name="rashan_number_save"),
    path('rashan/number/to/uid/status/',customerviews.rashannumbertatus,name='rashannumbertatus'),
    #CUSTOMER PATH FOR   PM KISHAN REGISTRATION NUMBER
    path('pm/registration/number/apply',customerviews.pmkishanregistrationnumberapply,name='pmkishanregistrationnumberapply'),
    path('pm/kishan/list/',customerviews.pmkishanregistrationnumberlist,name='pmkishanregistrationnumberlist'),
    path('pm/kishan/registration/number/save/',customerviews.pm_kishan_registration_number_save,name="pm_kishan_registration_number_save"),
    path('pmkishan/registration/status',customerviews.pmkishanregistrationtatus,name='pmkishanregistrationtatus'),
    #  CUSTOMER PATH FOR DL TO PDF
    path('dl/pdf/apply/',customerviews.dlpdfapply,name='dlpdfapply'),
    path('dl/pdf/save/',customerviews.dl_pdf_save,name="dl_pdf_save"),
    path('dl/pdf/list/',customerviews.dlpdflist,name='dlpdflist'),
    path('dl/pdf/status',customerviews.dlpdfstatus,name='dlpdfstatus'),
    # CUSTOMER PATH FOR FIND DL NUMBER
    path('find/dl/number/apply/',customerviews.finddlnumberapply,name='finddlnumberapply'),
    path('find/dl/number/list/',customerviews.finddlnumberlist,name='finddlnumberlist'),
    path('find/dl/number/save/',customerviews.find_dl_number_save,name="find_dl_number_save"),
    path('find/dl/number',customerviews.dlnumberstatus,name='dlnumberstatus'),
    # CUSTOMER PATH FOR AYUSHMAN CARD PDF
    path('ayushman/card/pdf/apply/',customerviews.ayushmancardpdfapply,name='ayushmancardpdfapply'),
    path('ayushman/card/pdf/list/',customerviews.findayushmancardpdflist,name='findayushmancardpdflist'),
    path('ayushman/card/pdf/save/',customerviews.find_ayushmancard_pdf_save,name="find_ayushmancard_pdf_save"),
    path('ayushman/card/status/',customerviews.ayushmancardstatus,name='ayushmancardstatus'),
    # CUSTOMER PATH FOR PM KISHAN PAYMENT DETAILS 
    path('pm/kishan/payment/details/apply/',customerviews.pmkishanregistpaymentapply,name='pmkishanregistpaymentapply'),
    path('pm/kishan/payment/details/list/',customerviews.findpmkishanpaymentdetaillist,name='findpmkishanpaymentdetaillist'),
    path('pm/kishan/payment/detail/save/',customerviews.find_pm_kishan_payment_details_save,name="find_pm_kishan_payment_details_save"),
    path('pmkishan/payment/status/',customerviews.pmkishapaymentstatus,name='pmkishapaymentstatus'),
    # CUSTOMER PATH FOR VICHEL RC PDF
    path('rc/pdf/apply/',customerviews.rcpdfapply,name='rcpdfapply'),
    path('rc/pdf/list/',customerviews.rcpdflist,name='rcpdflist'),
    path('rc/pdf/save/',customerviews.rc_pdf_save,name="rc_pdf_save"),
    path('rc/pdf/status',customerviews.rcpdfstatus,name='rcpdfstatus'),
    # CUSTOMER PATH FOR JOB CARD PDF APPLY
    path('job/card/pdf/apply',customerviews.jobcardpdfapply,name="jobcardpdfapply"),
    path('job/card/pdf/list/',customerviews.jobcardpdfist,name='jobcardpdfist'),
    path('job/card/pdf/save/',customerviews.jobcard_to_pdf_save,name="jobcard_to_pdf_save"),
    path('job/card/pdf/status',customerviews.jobcardpdfstatus,name='jobcardpdfstatus'),
    # IMPORTANT PATH LINK FOR ALL
    path('contactus/',views.contacus,name="contactus"),
    path("term&condition/",views.termandcondition,name="term_condition"),
    path('help/',views.help,name='help'),
    path('help/apply',views.help_apply,name='help_apply'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('about/us',views.aboutus,name='about_us'),
    path('privicy/policy/',views.privicypolicy,name='privicypolicy'),
    path('shiping/',views.shiping,name='shiping'),
    path('refund/cancel',views.refundcancel,name='refundcancel'),

]+ static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

