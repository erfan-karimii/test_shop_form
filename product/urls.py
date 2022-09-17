from django.urls import path
from . import views

app_name='poduct'

urlpatterns = [
    # path('',views.home,name='home'),
    path('list/',views.listview,name='listview'),
    path('search/؟mag=<mag>/',views.SearchView,name='SearchView'),
    path('list_order/<cat>',views.category_listview,name='category_listview'),
    path('detail/<id>/',views.DetailView,name='detailview'),
    path('color_ajax/',views.color_ajax,name='color_ajax'),
    path('size_ajax',views.size_ajax,name='size_ajax'),
]
