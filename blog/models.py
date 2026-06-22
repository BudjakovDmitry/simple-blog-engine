from django.db import models
from django.utils import timezone


class Series(models.Model):
    name = models.CharField(max_length=100)
    articles_in_series = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        PUBLISHED = "published"

    title = models.CharField(max_length=200)
    lead = models.TextField()
    slug = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    origin_text = models.TextField()
    formatted_text = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    views_count = models.IntegerField(default=0)
    series_id = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)

    def publish(self):
        self.status = self.Status.PUBLISHED
        self.published_at = timezone.now

    def unpublish(self):
        self.status = self.Status.DRAFT
        self.published_at = None

    def is_published(self):
        return self.status == self.Status.PUBLISHED

    def __str__(self):
        return self.title

class Views(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(default=timezone.now)
