from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1048576)
    title = models.CharField(max_length=256)
    link = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title


class Comments(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text


# class RepliesToComments(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     text = models.CharField(max_length=256)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
