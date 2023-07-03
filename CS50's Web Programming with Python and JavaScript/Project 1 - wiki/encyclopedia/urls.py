from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_entry/", views.new_entry, name="new_entry"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("update_entry/", views.update_entry, name="update_entry"),
    path("random_entry/", views.random_entry, name="random_entry")
]
