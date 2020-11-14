from django.http import JsonResponse
from django.views import View

from news.models import News, Comments

import json

# Create your views here.


class UserAPI(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {
                'id': request.user.pk,
                'username': request.user.username,
                'email': request.user.email,
            }
            return JsonResponse(data, safe=False)

        else:
            return JsonResponse({'error': 'user is not authenticated'}, safe=False)


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
                return JsonResponse({'error': 'there is no such specific news'}, safe=False, status=404)

        elif q:
            q = q.rstrip('/')
            news_with_q = News.objects.filter(title__contains=q).order_by('-created')
            return JsonResponse([news.as_dict() for news in news_with_q], safe=False)

        else:
            all_news = News.objects.all().order_by('-created')
            return JsonResponse([news.as_dict() for news in all_news], safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        link = 1
        all_links = list(News.objects.values_list('link', flat=True).order_by('link'))
        if all_links and all_links[0] == 1:
            for existing_link in all_links:
                if existing_link + 1 not in all_links:
                    link = existing_link + 1
                    break
        data['link'] = link

        if request.user.is_authenticated:
            data['user'] = request.user
        new_news = News.objects.create(**data)

        return JsonResponse(new_news.as_dict(), safe=False)

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)

        specific_news = News.objects.filter(link=data['link']).first()

        if specific_news:
            specific_news.delete()
        return JsonResponse(True, safe=False)


class CommentsAPI(View):
    def get(self, request, *args, **kwargs):
        news_link = int(request.GET.get('link'))

        specific_news = News.objects.filter(link=news_link).first()
        if not specific_news:
            return JsonResponse({'error': 'there is no such specific news'}, safe=False, status=404)

        all_comments = Comments.objects.filter(news=specific_news).order_by('-created')
        return JsonResponse([comment.as_dict() for comment in all_comments], safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        specific_news = News.objects.filter(link=data['news_link']).first()
        if not specific_news:
            return JsonResponse({'error': 'there is no such specific news'}, safe=False, status=404)

        del data['news_link']
        data['news'] = specific_news

        if request.user.is_authenticated:
            data['user'] = request.user
        comment = Comments.objects.create(**data)

        return JsonResponse(comment.as_dict(), safe=False)

    def delete(self, request, *args, **kwargs):
        comment_id = json.loads(request.body)['id']
        comment = Comments.objects.filter(pk=comment_id)

        if comment:
            comment.delete()
        return JsonResponse(True, safe=False)
