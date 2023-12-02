from django.urls import path
from . import views

urlpatterns = [
    path('', views.listPosts, name='list-posts'),
    path('create-forum-post/', views.createForumPost, name='create-forum-post'),
    path('view-post/<uuid:pk>', views.viewPost, name='view-post'),
]
