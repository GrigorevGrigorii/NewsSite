from django.http import JsonResponse
from django.views import View

from news.models import News, Comments

# Create your views here.


class NewsAPI(View):
    def get(self, request, *args, **kwargs):
        news_link = request.GET.get('link')
        q = request.GET.get('q')

        if news_link:
            news_link = int(news_link)
            specific_news = News.objects.filter(link=news_link).first()
            if specific_news is not None:
                return JsonResponse(specific_news.as_dict(), safe=False)
            else:
                return JsonResponse(False, safe=False, status=404)

        elif q:
            q = q.rstrip('/')
            news_with_q = News.objects.filter(title__contains=q).order_by('-created')
            return JsonResponse([news.as_dict() for news in news_with_q], safe=False)

        else:
            all_news = News.objects.all().order_by('-created')
            return JsonResponse([news.as_dict() for news in all_news], safe=False)

    def post(self, request, *args, **kwargs):
        title = request.GET.get('title')
        text = request.GET.get('text')
        link = 1

        all_links = list(News.objects.values_list('link', flat=True).order_by('link'))
        if all_links and all_links[0] == 1:
            for existing_link in all_links:
                if existing_link + 1 not in all_links:
                    link = existing_link + 1
                    break

        if request.user.is_authenticated:
            new_news = News.objects.create(text=text, title=title, link=link, user=request.user)
        else:
            new_news = News.objects.create(text=text, title=title, link=link)

        return JsonResponse(new_news.as_dict(), safe=False)

    def delete(self, request, *args, **kwargs):
        link = request.GET.get('link')
        specific_news = News.objects.filter(link=link).first()

        if specific_news:
            specific_news.delete()
        return JsonResponse(True, safe=False)


class CommentsAPI(View):
    def get(self, request, *args, **kwargs):
        news_link = int(request.GET.get('link'))

        specific_news = News.objects.filter(link=news_link).first()
        all_comments = Comments.objects.filter(news=specific_news).order_by('-created')
        return JsonResponse([comment.as_dict() for comment in all_comments], safe=False)

    def post(self, request, *args, **kwargs):
        text = request.GET.get('text')
        news_link = request.GET.get('news_link')

        specific_news = News.objects.filter(link=news_link).first()
        if not specific_news:
            return JsonResponse(False, safe=False, status=404)

        if request.user.is_authenticated:
            comment = Comments.objects.create(text=text, news=specific_news, user=request.user)
        else:
            comment = Comments.objects.create(text=text, news=specific_news)

        return JsonResponse(comment.as_dict(), safe=False)

    def delete(self, request, *args, **kwargs):
        comment_id = request.GET.get('id')
        comment = Comments.objects.filter(pk=comment_id)

        if comment:
            comment.delete()
        return JsonResponse(True, safe=False)
