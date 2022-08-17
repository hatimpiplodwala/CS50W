from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display, name="display"),
    path("search", views.search, name = "search"),
    path("random", views.randomentry, name = "random")
]
