from django.db import models

# Create your models here.


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1048576)
    title = models.CharField(max_length=64)
    link = models.IntegerField()
