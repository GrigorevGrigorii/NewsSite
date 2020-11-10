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

    def as_dict(self):
        return {
            'id': self.pk,
            'created': self.created,
            'text': self.text,
            'title': self.title,
            'link': self.link,
            'user_id': self.user.id if self.user is not None else ""
        }


class Comments(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

    def as_dict(self):
        return {
            'id': self.pk,
            'created': self.created,
            'text': self.text,
            'user_id': self.user.id if self.user is not None else "",
            'news_link': self.news.link
        }


# class RepliesToComments(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     text = models.CharField(max_length=256)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
