from django.shortcuts import render,get_object_or_404,redirect
from .models import Order,OrderDetail
from product.models import Product
from .forms import NewOrderForm
from django.http import HttpResponse
import json
from payment.models import PayedOrder , PayedOrderDetail
from django.utils import timezone
from account.models import Profile
from cryptography.fernet import Fernet
from account.forms import InfoForm
from Cart.forms import NewOrderForm
# Create your views here.
# f_obj = Fernet(Fernet.generate_key())

def add_user_order(request):
    form = NewOrderForm(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            order = Order.objects.filter(owner_id=request.user.id,is_paid=False).first()
            if order is None:
                order = Order.objects.create(owner_id=request.user.id,is_paid=False)

        product_id =form.cleaned_data['product_id']    
        color = form.cleaned_data['color']
        size =form.cleaned_data['size']
        count = form.cleaned_data['count']
        
        product = Product.objects.get(id=product_id)
        
        if count < 1 or count > product.tedad_mahsole : 
            return redirect('/cart/')
        
        price_color = 0
        try:
            x = product.color_set.get(color=color)
            price_color = x.Ekhtelaf
        except:
            pass
        price_size = 0
        try:
            x = product.size_set.get(size=size)
            price_size = x.Ekhtelaf
        except:
            pass
        total_price = price_color + price_size + product.main_discount_cal(inti=True)
        if request.user.is_authenticated:
            if order.orderdetail_set.filter(product=product,size=size,color=color):
                order.orderdetail_set.filter(
                    product=product
                ).update(count=count,size=size,color=color,price=total_price)
            else:
                order.orderdetail_set.create(
                    product=product,price=total_price,count=count,size=size,color=color
                )
            return redirect('/cart')
        else:
            try:
                x = request.COOKIES['OrderDetail']
                jsonstyle = json.loads(x)
                orderdetail = OrderDetail.objects.create(product=product,color=color,count=count,size=size,price=total_price)
                
                for x in jsonstyle:
                    if jsonstyle[x]['id'] == product_id:
                        print(jsonstyle[x]['size'],'testtttttttttttttt')
                        print(size)
                        if  jsonstyle[x]['color'] == color and jsonstyle[x]['size'] == size :
                            jsonstyle[x] = {'id':product_id,'color':color,'size':size,'count':count}
                            break
                        else :
                            jsonstyle[orderdetail.id] = {'id':product_id,'color':color,'size':size,'count':count}
                            break
                        
                    else:    
                        jsonstyle[orderdetail.id] = {'id':product_id,'color':color,'size':size,'count':count}
                        break
                else:
                    jsonstyle[orderdetail.id] = {'id':product_id,'color':color,'size':size,'count':count}
                
                orderdetail.delete()
                jsonstyle2 = json.dumps(jsonstyle)
                response = redirect('/cart')
                response.delete_cookie('OrderDetail')
                response.set_cookie('OrderDetail',jsonstyle2,172800)
                return response 
            except:
                order = Order.objects.create()
                orderdetail = OrderDetail.objects.create(product=product,color=color,count=count,size=size,price=total_price)
                x = {orderdetail.id:{'id':product_id,'color':color,'size':size,'count':count}}
                orderdetail.delete()
                jsonstyle = json.dumps(x)
                response = redirect('/cart')
                response.set_cookie('OrderDetail',jsonstyle,172800)
                response.set_cookie('Order',order.id,172800)
                order.delete()
                return response 
    else:
        print('test')
        return redirect('/')

def user_open_order(request):
    context = {
    'form': NewOrderForm() ,
    'order':None,
    'details':None,
    'total':0,
    'sum':0,
    }
    if request.user.is_authenticated:
        open_order = Order.objects.filter(owner_id=request.user.id,is_paid=False).first()
        # چک کنیم که تعداد محصول در یبد خرید بیشتر از موجودی نباشه
        for x in open_order.orderdetail_set.all():
            product = Product.objects.get(id=x.product.id)
            print(x.count)
            print(product.tedad_mahsole)
            if x.count > product.tedad_mahsole:
                x.count = product.tedad_mahsole
                x.save()
        ################################################################
        if open_order is not None:
            context['order'] = open_order
            context['details'] = open_order.orderdetail_set.all()
            # context ['sum'] =open_order.orderdetail_set.
            context['total'] = open_order.get_total_price()
    else:
        total_price = 0
        try:
            detail = request.COOKIES['OrderDetail']
            z = json.loads(detail)
            for det in z:
                id = z[det]['id']
                product = Product.objects.get(id=id)
                if z[det]['count'] > product.tedad_mahsole:
                    z[det]['count'] = product.tedad_mahsole

                price_color = 0
                try:
                    x = product.color_set.get(color=z[det]['color'])
                    price_color = x.Ekhtelaf
                except:
                    pass
                price_size = 0
                try:
                    x = product.size_set.get(size=z[det]['size'])
                    price_size = x.Ekhtelaf
                except:
                    pass
                total_price_single = price_color + price_size + product.main_discount_cal(inti=True)
                total_price += total_price_single * z[det]['count']

            context['details'] = z
            context['total'] = total_price
        except:
            print("erer")
        return render(request,'open_ano_order.html',context)


    return render(request,'user_open_order.html',context)

def remover_order_detail(request,id):
    # # order_detail = product_id
    # if product_id:
    #     order_detail = OrderDetail.objects.get(id=product_id)

    #     if order_detail:
    #         order_detail.delete()
    order = Order.objects.get(owner=request.user,is_paid=False)
    x = order.orderdetail_set.get(id=id)
    x.delete()
    return redirect('/cart')
 
def remove_from_cookie(request,id):
    x = request.COOKIES['OrderDetail']
    f = json.loads(x)
    del f[str(id)]
    m = json.dumps(f)
    response = redirect('/cart')
    response.delete_cookie('OrderDetail')
    response.set_cookie('OrderDetail',m,172800)
    return response

def order_payed(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        return redirect('/info/')
    order = Order.objects.get(owner=request.user,is_paid=False)
    order.is_paid = True
    order.payment_date = timezone.now()
    order.save()
    payed_order = PayedOrder.objects.create(
        owner = request.user,payment_date= order.payment_date,
        city = profile.city , address= profile.address,username= request.user.username
    )
    for detail in order.orderdetail_set.all():
        PayedOrderDetail.objects.create(
            order = payed_order , product=detail.product ,price = detail.price,
            color = detail.color, size= detail.size , count=detail.count,
            
        )
    return HttpResponse('paid')

def addressView(request):
    context = {
        'form':InfoForm,
        'prof':Profile.objects.filter(user=request.user).last(),
        'total':0,
    }
    open_order = Order.objects.filter(owner_id=request.user.id,is_paid=False).first()
    if open_order is not None:
        context['total'] = open_order.get_total_price()
    return render(request,'address.html',context)




def update_In_open_order(request):
    form = NewOrderForm(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated:
            order = Order.objects.filter(owner_id=request.user.id,is_paid=False).first()
        product_id =form.cleaned_data['product_id']    
        color = form.cleaned_data['color']
        size =form.cleaned_data['size']
        count = form.cleaned_data['count']
        
        product = Product.objects.get(id=product_id)
        
        if count < 1 or count > product.tedad_mahsole : 
            return redirect('/cart/')
        
        price_color = 0
        try:
            x = product.color_set.get(color=color)
            price_color = x.Ekhtelaf
        except:
            pass
        price_size = 0
        try:
            x = product.size_set.get(size=size)
            price_size = x.Ekhtelaf
        except:
            pass
        total_price = price_color + price_size + product.main_discount_cal(inti=True)
        if request.user.is_authenticated:
            if order.orderdetail_set.filter(product=product,size=size,color=color):
                order.orderdetail_set.filter(
                    product=product ,size=size,color=color,
                ).update(count=count,price=total_price)
            else:
                order.orderdetail_set.create(
                    product=product,price=total_price,count=count,size=size,color=color
                )
            return redirect('/cart')
        else:
            try:
                x = request.COOKIES['OrderDetail']
                jsonstyle = json.loads(x)
                orderdetail = OrderDetail.objects.create(product=product,color=color,count=count,size=size,price=total_price)
                
                for x in jsonstyle:
                    if jsonstyle[x]['id'] == product_id and jsonstyle[x]['color'] == color and jsonstyle[x]['size'] == size:
                        jsonstyle[x] = {'id':product_id,'color':color,'size':size,'count':count}
                
                orderdetail.delete()
                jsonstyle2 = json.dumps(jsonstyle)
                response = redirect('/cart')
                response.delete_cookie('OrderDetail')
                response.set_cookie('OrderDetail',jsonstyle2,172800)
                return response 
            except:
                order = Order.objects.create()
                orderdetail = OrderDetail.objects.create(product=product,color=color,count=count,size=size,price=total_price)
                x = {orderdetail.id:{'id':product_id,'color':color,'size':size,'count':count}}
                orderdetail.delete()
                jsonstyle = json.dumps(x)
                response = redirect('/cart')
                response.set_cookie('OrderDetail',jsonstyle,172800)
                response.set_cookie('Order',order.id,172800)
                order.delete()
                return response 
    else:
        print('test')
        return redirect('/')
