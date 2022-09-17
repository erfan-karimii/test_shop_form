from django.db import models
from account.models import MyUser
from product.models import Product
from colorfield.fields import ColorField

# Create your models here.
class PayedOrder(models.Model):
    owner = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,)
    username = models.CharField(max_length=400,)
    payment_date = models.DateTimeField(blank=True,null=True,)
    city = models.CharField(max_length=100,null=True,blank=True,)
    address = models.TextField(null=True,blank=True,)
    
    def __str__(self):
        return self.username

class PayedOrderDetail(models.Model):
    order = models.ForeignKey(PayedOrder,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    color = ColorField(null=True)
    size = models.CharField(max_length=20,null=True)
    count = models.IntegerField()
     
    def __str__(self):
        return self.product.name
