from django.contrib import admin
from .models import *
from django.forms import TextInput

# Register your models here.
class SizeInline(admin.TabularInline):
    model = Size
    extra = 0

class ColorInline(admin.TabularInline):
    model = Color
    extra = 0

class GalleryInline(admin.TabularInline):
    model = GalleryImage
    extra = 0

class CustomProduct(admin.ModelAdmin):
    inlines = [
        SizeInline,
        ColorInline,
        GalleryInline,
    ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'50'})},
    }

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product,CustomProduct)
admin.site.register(Company)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ZirTag)
admin.site.register(Zir_category)
admin.site.register(ProductTab)
admin.site.register(GalleryImage)