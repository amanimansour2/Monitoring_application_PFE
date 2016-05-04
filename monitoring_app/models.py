#from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username

class Machine(models.Model):
    name= models.CharField(default="Machine 1",max_length=30)
    address = models.CharField(default='168.85.69.4',max_length=12)
    username=models.CharField(default="Foulen",max_length=30)
    password= models.CharField(default="****",max_length=30,null=True)
    Prefix_freeswitch=models.CharField(default="1",max_length=5)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name 
class Call(models.Model):
    numerosrc = models.CharField(default="1000",max_length=50)
    addresssrc = models.CharField(default='192.168.3.5',max_length=12)
    numerodest =models.CharField(default="1010",max_length=30)
    addressdest =models.CharField(default="192.168.3.6",max_length=30)
    def __str__(self):
        return self.numerosrc 