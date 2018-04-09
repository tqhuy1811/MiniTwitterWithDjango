from django.db import models
from django import forms

from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
  profilePicture =  models.FileField(upload_to='userprofile',null=True)
  bio = models.TextField(null=True)
  birthday = models.DateField(null=True)

class Blog(models.Model):
  title = models.CharField(max_length=200)
  body = models.TextField()
  totalComment = models.IntegerField(null=True)
  totalLikes = models.IntegerField(null=True)
  dated_created = models.DateTimeField(auto_now=True)
  creator = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Comment(models.Model):
  body = models.TextField()
  dated_created = models.DateTimeField(auto_now=True)
  creator = models.ForeignKey(User,on_delete=models.CASCADE,default='')
  blog = models.ForeignKey(Blog,on_delete=models.CASCADE,default='')