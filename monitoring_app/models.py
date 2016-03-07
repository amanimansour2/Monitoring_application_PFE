#from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username
		
		
		
class Machine(models.Model):
    name = models.CharField(default="Machine 1",max_length=50)
    address = models.CharField(default='168.85.69.4',max_length=12)
    username=models.CharField(default="Foulen",max_length=30)
    password=models.CharField(default="****",max_length=30)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name 