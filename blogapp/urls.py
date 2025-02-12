from django.urls import path
from . import views 

urlpatterns = [
    path("",views.index, name= 'index'),
    path("article/<slug:slug>", views.details,name = 'details'),
    path("create/article", views.create_article, name="create-article"),
    path("update/article/<slug:slug>", views.update_article, name = "update-article"),
    path("delete_article/<slug:slug>", views.delete_article, name = "delete-article")
]