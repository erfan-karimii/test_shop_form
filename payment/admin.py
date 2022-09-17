from django.contrib import admin
from .models import PayedOrder ,PayedOrderDetail

# Register your models here.
class tab(admin.TabularInline):
    model = PayedOrderDetail
    extra = 0
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('order','product','price','color','size','count')
        return self.readonly_fields
    

class CustomPayedOrder(admin.ModelAdmin):
    inlines = [
        tab,
    ]
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('owner','username','payment_date','city','address')
        return self.readonly_fields

class CustomPayedOrderDetail(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ('order','product','price','color','size','count')
        return self.readonly_fields

admin.site.register(PayedOrderDetail,CustomPayedOrderDetail)
admin.site.register(PayedOrder,CustomPayedOrder)