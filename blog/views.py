from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render

from .controller import get_article_by_slug, get_last_articles, get_last_published
from .models import Article


def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        article_list = get_last_articles()
    else:
        article_list = get_last_published()

    context = {"article_list": article_list}
    return render(request, "blog/index.html", context)


def page(request, page):
    return HttpResponse(f"You're on the page {page}")


def read(request, slug):
    try:
        article = get_article_by_slug(slug)
    except Article.DoesNotExist as error:
        raise Http404("Article not found") from error

    if not request.user.is_authenticated or not request.user.is_superuser:
        if not article.is_published():
            raise PermissionDenied

    return render(request, "blog/article.html", {"article": article})
