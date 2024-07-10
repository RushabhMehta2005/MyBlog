from django.urls import path
from . import views

app_name = "BlogApp"
urlpatterns = [
    path("browse", views.browse, name="browse"),
    path("add_blog", views.add_blog, name="add_blog"),
    path("edit_blog/<int:blog_id>", views.edit_blog, name="edit_blog"),
    path("delete_blog/<int:blog_id>", views.delete_blog, name="delete_blog"),
    path("like/<int:blog_id>/", views.like_blog, name="like_blog"),
    path("comment/<int:blog_id>/", views.add_comment, name="add_comment"),
]
