from django.db import models

# Create your models here.
class User(models.Model):
	username=models.CharField(max_length=128)
	email=models.EmailField(unique=True)
	password=models.CharField(max_length=256)
	url=models.CharField(max_length=256,default="Url")
	register_time=models.DateTimeField(auto_now_add=True)
	update_time=models.DateTimeField(auto_now=True)