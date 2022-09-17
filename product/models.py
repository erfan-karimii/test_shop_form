from django.db import models
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Category(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام دسته بندی')
    text = RichTextField(null=True,blank=True,verbose_name='توضیح دسته بندی')

    def __str__(self):
        return self.name

class Zir_category(models.Model):
    sargroh = models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='سردسته')
    name = models.CharField(max_length=100,verbose_name='نام')


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ZirTag(models.Model):
    sargroh = models.ForeignKey(Tag,on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

class Company(models.Model):
    name = models.CharField(max_length=100,verbose_name='اسم کمپانی',null=True)
    image = models.ImageField(verbose_name='عکس کمپانی',null=True)
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس',null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]
    name = models.CharField(max_length=400)
    image = models.ImageField()
    alt = models.CharField(max_length=100,null=True)
    image_2 = models.ImageField(null=True)
    alt_2 = models.CharField(max_length=100,null=True)
    price_asli = models.IntegerField(verbose_name='قیمت اصلی',null=True)
    tedad_mahsole = models.PositiveBigIntegerField(null=True,verbose_name='تعداد محصول',validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    info = RichTextField()
    tags = models.ManyToManyField(Tag)                                                                                                      
    tedad_forosh = models.IntegerField(default=0)
    takhfif = models.IntegerField(null=True,validators=[MaxValueValidator(100),MinValueValidator(0)],verbose_name='درصد تخفیف')
    company = models.ForeignKey(Company,on_delete=models.PROTECT,null=True)
    color_asli = ColorField(samples=COLOR_PALETTE,null=True)
    size_asli = models.CharField(max_length=20,null=True)
    created  =models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def __add__(self, other):
        return self.price_asli + other
    
    def __eq__(self,other): 
        return self.price_asli == other

    def main_discount_cal(self,num=None,eq=None,inti=None):
        if inti:
            return int(self.price_asli - (self.price_asli * (self.takhfif/100)) )
        return self.price_asli - (self.price_asli * (self.takhfif/100))

    # def check_new(self):
        # now = datetime.datetime.now()
        # print(self.created - int(now.hour))
        # return  True if  self.created.hour - timezone.now().hour() > 3 else False

class Size(models.Model):
    product = models.ForeignKey(Product,null=True,on_delete=models.PROTECT)
    size = models.CharField(max_length=20,verbose_name='سایز')
    Ekhtelaf = models.IntegerField(verbose_name='اختلاف قیمت',null=True)

    class Meta:
        verbose_name='سایز های بیشتر'
        verbose_name_plural='سایز های بیشتر'

    def __str__(self):
        return self.size

class Color(models.Model):
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]
    product = models.ForeignKey(Product,null=True,on_delete=models.PROTECT)
    color = ColorField(samples=COLOR_PALETTE)
    Ekhtelaf = models.IntegerField(verbose_name='اختلاف قیمت',null=True) 

    class Meta:
        verbose_name='رنگ های بیشتر'
        verbose_name_plural='رنگ های بیشتر'
    

    def __str__(self):
        return self.product.name + " " + self.color
    
    def color_price_cal(self):
        return self.Ekhtelaf + self.product.price_asli - (self.product.price_asli * (self.product.takhfif/100))
    
class vizhegi(models.Model):
    image = models.FileField()
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=100)

class ProductTab(models.Model):
    name = models.CharField(max_length=100)
    text = RichTextField()
    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    image = models.ImageField(verbose_name='عکس محصول')
    alt= models.CharField(max_length=150,verbose_name='توضیحات عکس')

# class ModelComment(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='نام مقاله')
#     name = models.CharField(max_length=300,verbose_name='نام شخص')
#     Email_address = models.EmailField(max_length=254,verbose_name='ادرس ایمیل')
#     massage = models.TextField(verbose_name='پیام')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=False,verbose_name='نمایش داده شود؟')
#     ip = models.ForeignKey(IPAddress,on_delete=models.CASCADE,null=True,verbose_name='')
    
#     class Meta:
#         verbose_name='کامنت'
#         verbose_name_plural="کامنت ها"
#         ordering = ['-created']

#     def __str__(self):
#         return self.name

# class AnswerProduct(models.Model):
#     commentblog = models.ForeignKey(ModelComment,on_delete=models.PROTECT,verbose_name='نام مقاله')
#     name = models.CharField(max_length=300,verbose_name='نام شخص')
#     Email_address = models.EmailField(max_length=254,verbose_name='ادرس ایمیل')
#     massage = models.CharField(max_length=500,verbose_name='پیام')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=False,verbose_name='نمایش داده شود؟')
#     class Meta:
#         verbose_name=''
#         verbose_name_plural='پاسخ کامنت ها'
#         ordering = ['-created']

