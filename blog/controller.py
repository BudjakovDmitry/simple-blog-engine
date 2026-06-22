from django.db.models.functions import Coalesce

from .models import Article


DEFAULT_ARTICLES_LIMIT = 10


def order_by_publication_date(queryset):
    return queryset.alias(sort_date=Coalesce("published_at", "created_at")).order_by("-sort_date")


def get_last_articles(count: int = DEFAULT_ARTICLES_LIMIT):
    return order_by_publication_date(Article.objects.all())[:count]


def get_last_published(count: int = DEFAULT_ARTICLES_LIMIT):
    return order_by_publication_date(
        Article.objects.filter(status=Article.Status.PUBLISHED)
    )[:count]


def get_article_by_slug(slug: str) -> Article:
    return Article.objects.get(slug=slug)
