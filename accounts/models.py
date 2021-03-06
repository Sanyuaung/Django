from typing import Text
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile_pic=models.ImageField(null=True,blank=True,upload_to="static/profiles",default="static/profiles/default.png ")
    email=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category=(
        ('indoor','In Door'),
        ('outdoor','Out Door')
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=category)
    description=models.CharField(max_length=200,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name 

class Order(models.Model):
    status=(
        ('pending','Pending'),
        ('out of delivery','Out For Delivery'),
        ('delivered','Delivered') 
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,null=True,choices=status)


    def __str__(self):
        return self.product.name 