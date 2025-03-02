from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:page>", views.display, name="display"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("<str:page>/edit/", views.edit, name="edit")
]
