from product.models import Product
from django.shortcuts import render,redirect
import random
from .models import Profile,MyUser
from django.contrib import messages
from kavenegar import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import make_password
from .forms import InfoForm,PhoneNumber
import json
from Cart.models import Order,OrderDetail
# Create your views here.
def registerView(request):
    if request.user.is_authenticated :
        return redirect('/')
    return render(request,'account/register.html',{})

# def loginView(request):
#     return render(request,'account/login.html')

def send_sms_test(request):
    number = random.randint(1000, 9999)
    if request.method == "POST":
        form=PhoneNumber(request.POST)
        if form.is_valid():

            phone =form.cleaned_data['phone']
            if MyUser.objects.filter(phone=phone):
                MyUser.objects.filter(phone=phone).update(token=number)
            else:
                MyUser.objects.create(username=phone,phone=phone,token=number)
            print(number)
            api = KavenegarAPI('4D526E3432522F42744D47414B3845436D59734377572B71645A455565644575')
            params = { 'sender' : '10000080808880', 'receptor': f'{phone}', 'message' :f'{number}' }
            try:
                api.sms_send( params)
            except:
                messages.success(request,'درست وارد کنید')
                return render(request,'account/register.html')

            response = render(request,'account/verify.html')
            
            response.set_cookie('phone_number_cookie',phone,1000)
            return response
        else:
            messages.success(request,'درست وارد کنید')
            return render(request,'account/register.html')
    else :
        return render(request,'account/register.html')

def VerifyChecked(request):
    if request.method == "POST":
        token = request.POST.get('token')
        phone_c = request.COOKIES['phone_number_cookie']
        #----------------------------------------
        try :
            user = MyUser.objects.get(phone= phone_c)
        except:
            messages.success(request,'شما اکانتی با این شماره ندارید')
        if user.token == token :
            MyUser.objects.filter(phone=phone_c).update(is_verify=True)
            return render(request,'account/complateprofile.html')
        else :
            messages.success(request,'کدارسالی را درست وارد کنید')
        return redirect('/')
    return render(request,'account/complateprofile.html')


def ComplateProfileView(request):
    return render(request,'account/complateprofile.html',{})

def ComplateProfile(request):
    if request.method == "POST":
        # username=request.POST.get('username')
        password = request.POST.get('password')
        phone_c = request.COOKIES['phone_number_cookie']
        MyUser.objects.filter(phone=phone_c).update(
            username=phone_c,password=make_password(password)
        )
        messages.success(request,'پروفایل شما با موفقیت ساخته شد')
        user = MyUser.objects.get(username=phone_c)
        if user.is_verify:
            login(request, user)
    return redirect('/')

def respass(request):
    return render(request,'account/eghdam.html')


def SendSmsReset(request):
    number = random.randint(1000, 9999)
    print(number)
    if request.method == "POST":
        phone = request.POST.get('phone')
        if MyUser.objects.filter(phone=phone):
            MyUser.objects.filter(phone=phone).update(token=number)
        else:
            messages.success(request,'شما هیج اکانتی ندارید')
    else:
        return render(request,'account/verify2.html')

    api = KavenegarAPI('4D526E3432522F42744D47414B3845436D59734377572B71645A455565644575')
    params = {'sender' : '10000080808880', 'receptor': f'{phone}', 'message' :f'{number}' }
    api.sms_send( params)
    response = render(request,'account/verify2.html')
    x =phone
    response.set_cookie('phone_number_cookie',x,1000)
    return response

def ResetProfileView(request):
    return render(request,'account/ResetPasswordView.html',{})

def ResetProfile(request):
    if request.method == "POST":
        # username=request.POST.get('username')
        password = request.POST.get('password')
        phone_c = request.COOKIES['phone_number_cookie']
        MyUser.objects.filter(phone=phone_c).update(
            password=make_password(password)
        )
        messages.success(request,'عملیات با موفقیت انجام شد')
    return redirect('/')

def VerifyChecked2(request):
    if request.method == "POST":
        token = request.POST.get('token')
        phone_c = request.COOKIES['phone_number_cookie']
        try :
            user = MyUser.objects.get(phone= phone_c)
        except:
            messages.success(request,'شما اکانتی با این شماره ندارید')

        if user.token == token :
            return render(request,'account/ResetPasswordView.html')
        else:
            messages.success(request,'!!! کدارسالی را درست وارد کنید')
        return redirect('/')
    return render(request,'account/ResetPasswordView.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verify:
                login(request, user)
                
                if Order.objects.filter(owner=request.user,is_paid=False).last():
                    pass
                else:
                    try:
                        orderdetail=request.COOKIES['OrderDetail']
                        order=request.COOKIES['Order']
                        orderdetail = json.loads(orderdetail)
                        order = json.loads(order)
                        sabad = Order.objects.create(
                            id=order,owner=request.user
                        )
                        for x in orderdetail:
                            product=Product.objects.get(id=orderdetail[x]['id'])
                            color =orderdetail[x]['color']
                            size = orderdetail[x]['size']
                            price_color = 0
                            try:
                                m = product.color_set.get(color=color)
                                price_color = m.Ekhtelaf
                            except:
                                pass

                            price_size = 0
                            try:
                                m = product.size_set.get(size=size)
                                price_size = m.Ekhtelaf
                            except:
                                pass
                            total_price =  price_size + price_color + product.main_discount_cal(inti=True)
                            
                            OrderDetail.objects.create(
                                order=sabad,product=product,size = size, count =orderdetail[x]['count'],color=color,price=total_price
                                )
                    
                        response = redirect("/cart/")
                        response.delete_cookie('OrderDetail')
                        response.delete_cookie('Order')
                        return response
                    except KeyError:
                        pass
                return redirect('/')
            else:
                messages.success(request,"شما احراز هویت نشده ایید")

    form = AuthenticationForm()
    return render(request,'account/login.html',{'form':form})



def infoUser(request):
    if request.method == "POST":
        if request.POST.get('btn1'):
            form = InfoForm(request.POST)
            if form.is_valid():
                city = form.cleaned_data['city']
                address = form.cleaned_data['address']
                province = form.cleaned_data['province']
                receiver_name = form.cleaned_data['receiver_name']
                code_posty = form.cleaned_data['code_posty']
                code_meli = form.cleaned_data['code_meli']

                if Profile.objects.filter(user=request.user):
                    Profile.objects.filter(user=request.user).update(
                        address=address,code_meli=code_meli,city=city,code_posty=code_posty,
                        receiver_name=receiver_name,province=province
                        )
                else:
                    Profile.objects.create(
                        user=request.user,address=address,code_meli=code_meli,city=city,
                        code_posty=code_posty,receiver_name=receiver_name,province=province
                    )
                return redirect('/address')
        elif request.POST.get('btn2'):
            form = InfoForm(request.POST)
            if form.is_valid():
                city = form.cleaned_data['city']
                address = form.cleaned_data['address']
                province = form.cleaned_data['province']
                receiver_name = form.cleaned_data['receiver_name']
                code_posty = form.cleaned_data['code_posty']
                code_meli = form.cleaned_data['code_meli']

                if Profile.objects.filter(user=request.user):
                    Profile.objects.filter(user=request.user).update(
                        address=address,code_meli=code_meli,city=city,code_posty=code_posty,
                        receiver_name=receiver_name,province=province
                        )
                else:
                    Profile.objects.create(
                        user=request.user,address=address,code_meli=code_meli,city=city,
                        code_posty=code_posty,receiver_name=receiver_name,province=province
                    )
    else:
        form = InfoForm()

    context = {
        'user':request.user,
        'x':Profile.objects.filter(user=request.user).last()   
    }
    return render(request,'account/info.html',context)


def LogOut(request):
    logout(request)
    return redirect('/')