from django.contrib import admin
from .models import NavAsli , TagNav , SiteSetting,Tabligh , Slider,FooterAsli,FooterZir
# Register your models here.
class CustomNavAsli(admin.ModelAdmin):
    list_display = ('name','parent')
    list_editable = ('parent',)

class CustomSiteSetting(admin.ModelAdmin):
    list_display = ('name','active')

admin.site.register(TagNav)
admin.site.register(NavAsli,CustomNavAsli)
admin.site.register(SiteSetting,CustomSiteSetting)
admin.site.register(Tabligh)
admin.site.register(Slider)
admin.site.register(FooterAsli)
admin.site.register(FooterZir)


