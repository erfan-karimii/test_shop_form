from urllib import request
from django.urls import path
from . import views 

app_name='account'

urlpatterns = [
    path('register/',views.registerView,name='registerView'),
    path('login/',views.Login,name='login'),
    path('sendsms1/',views.send_sms_test,name='send'),
    path('VerifyChecked/',views.VerifyChecked,name='verify'),
    path('complateprofile/',views.ComplateProfileView,name='comp'),
    path('complateform/',views.ComplateProfile,name='complate'),
    path('resetpassword/',views.respass,name='resetpasswordsms'),
    path('sendsms2/',views.SendSmsReset,name='send2'),
    path('Change/',views.VerifyChecked2,name='changepass'),
    path('Changepassword2/',views.ResetProfile,name='resetprofile'),
    path('info/',views.infoUser,name='info'),
    path('logout/',views.LogOut,name='logout'),

]


