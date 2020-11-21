from django.http import JsonResponse
from django.views import View

from news.models import News, Comments

import json
from datetime import datetime

# Create your views here.


class UserAPI(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {
                'id': request.user.pk,
                'username': request.user.username,
                'email': request.user.email,
                'is_authenticated': True,
            }
            resp = JsonResponse(data, safe=False)
            resp.setdefault('Access-Control-Allow-Origin', '*')
            return resp

        else:
            resp = JsonResponse({'is_authenticated': False}, safe=False)
            resp.setdefault('Access-Control-Allow-Origin', '*')
            return resp


class NewsAPI(View):
    def get(self, request, *args, **kwargs):
        news_link = request.GET.get('link')

        if news_link:
            news_link = int(news_link)
            specific_news = News.objects.filter(link=news_link).first()
            if specific_news is not None:
                resp = JsonResponse(specific_news.as_dict(), safe=False)
                resp.setdefault('Access-Control-Allow-Origin', '*')
                return resp
            else:
                resp = JsonResponse({'error': 'there is no such specific news'}, safe=False, status=404)
                resp.setdefault('Access-Control-Allow-Origin', '*')
                return resp

        q = request.GET.get('q').rstrip('/') if request.GET.get('q') else ''
        grouped = request.GET.get('grouped')

        all_news = News.objects.filter(title__contains=q).order_by('-created')

        if grouped and grouped.rstrip('/').lower() == "true":
            grouped_news = []

            for news in all_news:
                created = news.created.strftime("%Y-%m-%d")
                all_groupers = list(map(lambda item: item['grouper'], grouped_news))
                if created not in all_groupers:
                    grouped_news.append({'grouper': created, 'list': [news.as_dict()]})
                else:
                    group = list(filter(lambda item: item['grouper'] == created, grouped_news))[0]
                    group['list'].append(news.as_dict())

            resp = JsonResponse(grouped_news, safe=False)
            resp.setdefault('Access-Control-Allow-Origin', '*')
            return resp

        resp = JsonResponse([news.as_dict() for news in all_news], safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        return resp

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

        resp = JsonResponse(new_news.as_dict(), safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        return resp

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)

        specific_news = News.objects.filter(link=data['link']).first()

        if specific_news:
            specific_news.delete()

        resp = JsonResponse(True, safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        return resp
    
    def options(self, request, *args, **kwargs):
        resp = JsonResponse({'status': 'ok'}, safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        resp.setdefault('Access-Control-Allow-Headers', 'Content-Type')
        return resp


class CommentsAPI(View):
    def get(self, request, *args, **kwargs):
        news_link = int(request.GET.get('link'))

        specific_news = News.objects.filter(link=news_link).first()
        if not specific_news:
            resp = JsonResponse({'error': 'there is no such specific news'}, safe=False, status=404)
            resp.setdefault('Access-Control-Allow-Origin', '*')
            return resp

        all_comments = Comments.objects.filter(news=specific_news).order_by('-created')

        resp = JsonResponse([comment.as_dict() for comment in all_comments], safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        return resp

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        specific_news = News.objects.filter(link=data['news_link']).first()
        if not specific_news:
            resp = JsonResponse({'error': 'there is no such specific news'}, safe=False, status=404)
            resp.setdefault('Access-Control-Allow-Origin', '*')
            return resp

        del data['news_link']
        data['news'] = specific_news

        if request.user.is_authenticated:
            data['user'] = request.user
        comment = Comments.objects.create(**data)

        resp = JsonResponse(comment.as_dict(), safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        return resp

    def delete(self, request, *args, **kwargs):
        comment_id = json.loads(request.body)['id']
        comment = Comments.objects.filter(pk=comment_id)

        if comment:
            comment.delete()

        resp = JsonResponse(True, safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        return resp
    
    def options(self, request, *args, **kwargs):
        resp = JsonResponse({'status': 'ok'}, safe=False)
        resp.setdefault('Access-Control-Allow-Origin', '*')
        resp.setdefault('Access-Control-Allow-Headers', 'Content-Type')
        return resp
