from django.shortcuts import render

from Cart.models import Order
# Create your views here.
from .models import NavAsli ,Slider, SiteSetting , FooterAsli , Tabligh
from product.models import Company , Product
def home(request):
    context= {
        'sliders' : Slider.objects.all(),
        'sitesetting' : SiteSetting.objects.filter(active = True).last(),
        'companys' : Company.objects.all(),
        'last_product_1': Product.objects.all().order_by('-created')[:4],
        'last_product_2': Product.objects.all().order_by('-created')[4:8],
    }
    return render(request,'index.html',context)

def header(request):

    context = {
        'navaslis' : NavAsli.objects.all(),
        'tabligh' : Tabligh.objects.all().last(),
        'sitesetting' : SiteSetting.objects.filter(active = True).last(),
    }
    return render(request,'header.html',context)

def footer(request):
    context = {
        'footeraslis' : FooterAsli.objects.all(),
        'sitesetting' : SiteSetting.objects.filter(active = True).last(),
    }
    return render(request,'footer.html',context)

