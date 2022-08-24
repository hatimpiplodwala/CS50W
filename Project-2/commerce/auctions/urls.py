from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("create", views.createlisting, name="create"),
    path("listing/<int:i>", views.listing_view, name="listing"),
    path("makebid/<int:i>", views.makebid, name="makebid"),
    path("alterwatchlist/<int:i>", views.alterwatchlist, name="alterwatchlist"),
    path("addcomment/<int:i>", views.addcomment, name="addcomment"),
    path("closebid/<int:i>", views.closebid, name="closebid"),
    path("viewwatchlist", views.viewwatchlist, name="viewwatchlist"),
    path("winsandbids", views.viewwinsbids, name="viewwinsbids"),
    path("mylistings", views.viewmylistings, name="viewmylistings")
]
