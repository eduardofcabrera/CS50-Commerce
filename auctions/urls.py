from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("watchlist", views.watchList, name="watchList"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categoryPage, name="category"),
    path("listing/<int:auctionID>", views.auctionPage, name="auctionPage"),
    path("listing/<int:auctionID>/finish", views.finishListing, name="finishListing"),
    path("listing/<int:auctionID>/comment", views.makeComment, name="makeComment"),
    path("listing/<int:auctionID>/<str:mode>", views.addRemoveWatchList, name="addRemoveWatchList")
]

