from django.core.exceptions import PermissionDenied
from django.db.models.functions import Coalesce
from django.db.models import F

from .models import Article, Stream


DEFAULT_ARTICLES_LIMIT = 10

# Feed

def order_by_publication_date(queryset):
    return (
        queryset.alias(sort_date=Coalesce("published_at", "created_at"))
        .order_by("-sort_date")
    )


def get_last_articles(
    published_only: bool = True,
    count: int = DEFAULT_ARTICLES_LIMIT,
    stream: str | None = None,
):
    articles = Article.objects.all()
    if published_only:
        articles = articles.filter(status=Article.Status.PUBLISHED)
    if stream:
        articles = articles.filter(stream__route=stream)

    return order_by_publication_date(articles)[:count]

# Article

def can_read_article(user, article: Article) -> bool:
    if article.is_published():
        return True

    return user.is_authenticated and user.is_superuser


def increment_article_views(article: Article) -> None:
    Article.objects.filter(pk=article.pk).update(
        views_count=F("views_count") + 1,
    )


def read_article(slug: str, user) -> Article:
    article = get_article_by_slug(slug)
    if not can_read_article(user, article):
        raise PermissionDenied

    increment_article_views(article)

    return article


def get_article_by_slug(slug: str) -> Article:
    return Article.objects.get(slug=slug)

# Streams

def get_streams():
    return Stream.objects.order_by("order")
