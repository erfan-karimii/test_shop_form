from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class MyUser(AbstractUser):
    phone = models.CharField(max_length=11,blank=True,null=True)
    token = models.CharField(max_length=10,blank=True,null=True)
    is_verify = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.PROTECT)
    province = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    code_posty = models.CharField(max_length=20,null=True,blank=True)
    receiver_name= models.CharField(max_length=250,null=True,blank=True)
    code_meli = models.CharField(max_length=20,null=True,blank=True)


    def __str__(self):
        return str(self.user)

