from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:page>/", views.page, name="page"),
    path("articles/<str:slug>/", views.read, name="read"),
]

