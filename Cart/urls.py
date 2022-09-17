from django.urls import path 
from . import views

app_name='Cart'

urlpatterns = [
    path('add_user_order/',views.add_user_order,name='add_user_order'),
    path('cart/',views.user_open_order,name='user_open_order'),
    path('remove/<int:id>/',views.remover_order_detail,name='remove'),
    path('removecookie/<int:id>/',views.remove_from_cookie,name='removeck'),
    path('paid/',views.order_payed,name='paid'),
    path('address/',views.addressView,name='address'),
    path('update_In/',views.update_In_open_order,name='update_In_open_order'),
]



