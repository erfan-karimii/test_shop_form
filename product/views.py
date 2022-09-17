import json
from django.shortcuts import render , get_object_or_404
from django.http import  JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import SearchForm
from .models import Color, Company, Product,Category , vizhegi , Size , ProductTab
from home.models import SiteSetting
from Cart.forms import NewOrderForm
# Create your views here.

def listview(request):
    products=Product.objects.filter(is_active=True)
    paginate_number = 4 # Show 2 contacts per page.
    paginator = Paginator(products, paginate_number) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products':page_obj,
        'products_size':Product.objects.filter(is_active=True).values('size_asli').distinct(),
        'categorys':Category.objects.all(),
        'colors':Color.objects.all(),
        'sizes' : Size.objects.all().values('size').distinct(),
        'companys':Company.objects.all(),
        'sitesetting' : SiteSetting.objects.filter(active=True).last(),
        'paginate_number':paginate_number,
    }
    return render(request,'listview.html',context)

def category_listview(request,cat):
    products=Product.objects.filter(is_active=True,category__name=cat)
    paginator = Paginator(products, products.count()) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products':page_obj,
        'categorys':Category.objects.all(),
        'colors':Color.objects.all(),
        'companys':Company.objects.all(),
        'sitesetting' : SiteSetting.objects.filter(active=True).last(),
        'cat' : Category.objects.get(name=cat)
    }
    return render(request,'listview.html',context)

def SearchView(request,mag):
    x = Product.objects.filter(Q(tags__name__icontains=mag)).distinct()    
    paginator = Paginator(x, x.count())
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
    'products':page_obj,
    'categorys':Category.objects.all(),
    'colors':Color.objects.all(),
    'companys':Company.objects.all(),
    'sitesetting' : SiteSetting.objects.filter(active=True).last(),
    'paginate_number': x.count(),
    
    }
    return render(request,'listview.html',context)

def DetailView(request,id):
    product = get_object_or_404(Product,id=id)
    form = NewOrderForm(request.POST or None,initial={'product_id':product.id})
    context = {
        'product':product,
        'vizhegi':vizhegi.objects.all(),
        'products':Product.objects.filter(is_active=True),
        'producttabs':ProductTab.objects.all(),
        'form' : form,
    }
    if not request.user.is_authenticated:
        try:
            m=request.COOKIES['OrderDetail']
            details = json.loads(m)
            context['color_a'] = details[product.id]['color']
            context['size_a'] = details[product.id]['size']
        except KeyError:
            pass
    
    return render(request,'detailview.html',context)
 
def color_ajax(request):
    color_id = request.GET.get('color_id')
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id = product_id)
        color =product.color_set.get(id = color_id)
        add_price = color.Ekhtelaf
    except:
        add_price = 0
    return JsonResponse({'add_price': add_price })

def size_ajax(request):
    size_id = request.GET.get('size_id')
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id = product_id)
        size =product.size_set.get(id = size_id)
        add_price = size.Ekhtelaf
    except:
        add_price = 0
    return JsonResponse({'add_price': add_price })


