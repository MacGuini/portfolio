from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

def listPosts(request):
    posts = Post.objects.all()
    return render(request, 'forum/list_posts.html', {'posts':posts})

def createForumPost(request):
    profile = request.user.profile
    form = PostForm()
    if request.method == "POST":
        
        form = PostForm(request.POST)
        if form.is_valid():
            
            forum = form.save(commit=False)
            forum.author = profile
            form.save()
            return redirect(request.GET['next'] if 'next' in request.GET else 'index')

    return render(request, 'forum/create_forum_post.html', {'form':form})

def viewPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'forum/view_post.html', {'post':post})

    

