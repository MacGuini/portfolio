from django.urls import path
from . import views

urlpatterns = [
    path('', views.listPosts, name='list-posts'),
    path('create-forum-post/', views.createForumPost, name='create-forum-post'),
    path('view-post/<uuid:pk>', views.viewPost, name='view-post'),
    path('post/<uuid:pk>/comment/', views.viewPost, name='comment'),
    path('post/<uuid:pk>/comment/<uuid:parent_comment_id>/', views.viewPost, name='reply'),
    path('edit-post/<uuid:pk>/', views.editPost, name="edit-post"),
    path('update-comment/<uuid:comment_id>/', views.updateComment, name='update-comment'),

]
