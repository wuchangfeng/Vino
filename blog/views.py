#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from blog.models import Article, Category, Tag
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.staticfiles.templatetags.staticfiles import static

class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = Article.objects.filter(status='p')
        return articles

    def get_context_data(self, **kwargs):
        kwargs['title'] = '首页'
        return super(IndexView, self).get_context_data(**kwargs)


# 分类视图
class CategoryView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        category_id = int(self.kwargs['category_id'])
        if category_id == 0:
            articles = Article.objects.filter(category__isnull=True, status='p')
        else:
            articles = Article.objects.filter(category=category_id, status='p')
        return articles

    def get_context_data(self, **kwargs):
        try:
            kwargs['title'] = '分类:' + Category.objects.filter(pk=self.kwargs['category_id'])[0].title
        except IndexError:
            kwargs['title'] = '没有找到这个分类!'
        return super(CategoryView, self).get_context_data(**kwargs)


# 标签视图
class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = Article.objects.filter(tag=self.kwargs['tag_id'], status='p')
        return articles

    def get_context_data(self, **kwargs):
        try:
            kwargs['title'] = '标签:' + Tag.objects.filter(pk=self.kwargs['tag_id'])[0].title
        except IndexError:
            kwargs['title'] = '没有找到标签!'
        return super(TagView, self).get_context_data(**kwargs)


# 文章详情视图
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/post.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'


    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        if obj.status == 'p':
            obj.viewed()
            return obj

    def get_context_data(self, **kwargs):
        kwargs['title'] = super(ArticleDetailView, self).get_object().title
        return super(ArticleDetailView, self).get_context_data(**kwargs)

def about_me(request) :
    return render(request, 'blog/about_me.html')

def comments(request) :
    return render(request, 'blog/comments.html')

def archives(request) :
    article_list = Article.objects.filter(status='p')
    #return render(request, 'blog/archives.html')
    return render(request, 'blog/archives.html', {'article_list' : article_list})

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response