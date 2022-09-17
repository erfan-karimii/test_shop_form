from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Tabligh(models.Model):
    text = models.CharField(max_length=400)
    link = models.URLField(blank=True)
    def __str__(self):
        return self.text

class TagNav(models.Model):
    name = models.CharField(max_length=100,verbose_name='تگ ها')    
    def __str__(self):
        return self.name

class TagNewPage(models.Model):
    name = models.CharField(max_length=100,verbose_name='تگ ها')    
    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    name = models.CharField(max_length=50,verbose_name='اسم سایت')
    logo = models.FileField(null=True,verbose_name='لوگو')
    alt = models.CharField(max_length=100,null=True,verbose_name='توضیحات لوگو')
    favicon = models.FileField(null=True,verbose_name='آیکون')
    alt2 = models.CharField(max_length=100,null=True,verbose_name='توضیحات icon')
    text = models.CharField(max_length=500,null=True,verbose_name='متن')
    text_vasat_nav = models.CharField(max_length=100,null=True,verbose_name='متن وسط نوبار') 
    image_bg = models.ImageField(null=True,verbose_name='عکس بک گراند صفحات داخلی')
    alt_bg = models.CharField(max_length=100,null=True,verbose_name='توضیح عکس بک گراند')
    telephon = models.CharField(max_length=30,null=True,verbose_name='تلفن')
    email= models.EmailField(max_length=100,null=True,verbose_name='ایمیل')
    address = models.CharField(max_length=200,null=True,verbose_name='ادرس')
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False,verbose_name='نمایش داده شود؟')

    def __str__(self):
        return self.name


class NavAsli(models.Model):
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,blank=True,null=True,default=None)
    name = models.CharField(max_length=50,verbose_name='نام')
    link = models.CharField(max_length=100,blank=True,null=True,verbose_name='ادرس صفحه')
    body = RichTextUploadingField(null=True,blank=True,verbose_name='بدنه')
    url_title = models.CharField(null=True,blank=True,max_length=300,verbose_name='نام صفحه')
    text = models.TextField(null=True,blank=True,verbose_name='متن')
    tag = models.ManyToManyField(TagNav,blank=True,verbose_name='تگ ها')

    class Meta:
        verbose_name='نوبار'
        verbose_name_plural='نوبارها'
        ordering = ['name']

    def __str__(self):
        return self.name

class Slider(models.Model):
    DIR = (
        ('right','right'),
        ('center','center'),
        ('left','left')
    )
    text_bold = models.CharField(max_length=300,verbose_name='متن بولد')
    text_simple = models.CharField(max_length=300,null=True,verbose_name='متن ساده')
    text_dir = models.CharField(max_length=20,choices=DIR,verbose_name='پوزیشن متن')
    image = models.ImageField(verbose_name='عکس سلایدر')
    alt = models.CharField(max_length=100,verbose_name='توضیح عکس')
    name_button = models.CharField(max_length=100,verbose_name='متن دکمه')
    link = models.CharField(max_length=100,blank=True,null=True,verbose_name='ادرس صفحه')
    body = RichTextUploadingField(null=True,blank=True,verbose_name='بدنه')
    url_title = models.CharField(null=True,blank=True,max_length=300,verbose_name='نام صفحه')
    text = models.TextField(null=True,blank=True,verbose_name='متن')
    tag = models.ManyToManyField(TagNewPage,blank=True,verbose_name='تگ ها')
    
    def __str__(self):
        return self.name_button + " | " + self.link


class FooterAsli(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class FooterZir(models.Model):
    footer = models.ForeignKey(FooterAsli,on_delete=models.PROTECT)
    name = models.CharField(max_length=50,verbose_name='نام')
    link = models.CharField(max_length=100,null=True,verbose_name='لینک صفحه')
    body = RichTextUploadingField(null=True,blank=True,verbose_name='بدنه')
    url_title = models.CharField(null=True,blank=True,max_length=300,verbose_name='نام صفحه')
    text = models.TextField(null=True,blank=True,verbose_name='متن')
    tag = models.ManyToManyField(TagNav,blank=True,verbose_name='تگ ها')
    def __str__(self):
        return  str(self.footer.name) + " | " +  self.name + " | " + self.link

