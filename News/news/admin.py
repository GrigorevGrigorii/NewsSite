from django.contrib import admin
from .models import News
# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    fields = ('created', 'title', 'text', 'link')


admin.site.register(News, NewsAdmin)
