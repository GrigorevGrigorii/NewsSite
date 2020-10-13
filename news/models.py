from django.db import models

# Create your models here.


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1048576)
    title = models.CharField(max_length=256)
    link = models.IntegerField(primary_key=True)


class Comments(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2048)
    username = models.CharField(max_length=150)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
