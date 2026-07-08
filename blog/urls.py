from django.urls import path

from . import views


urlpatterns = [
    path("", views.feed, name="feed"),
    path("frontend", views.frontend, name="frontend"),
    path("python", views.python, name="python"),
    path("articles/<str:slug>/", views.read, name="read"),
]
