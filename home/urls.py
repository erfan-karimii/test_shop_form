from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path('',views.home,name='home'),
    path('header/',views.header,name='header'),
    path('footer/',views.footer,name='footer')
]

