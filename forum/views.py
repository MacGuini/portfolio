import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from forum import mail_control

# Create your views here.

def listPosts(request):
    posts = Post.objects.all()
    return render(request, 'forum/list_posts.html', {'posts':posts})

@login_required(login_url='login')
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

#NOTE: depth and max_depth are used to control the amount of replies in some fashion. Will work on using these for something in the future.
def build_comment_tree(comments, depth=0, max_depth=10):
    comment_tree = []
    for comment in comments.order_by('created'):
        # Add the comment and its replies to the tree
        node = {
            'comment': comment,
            'depth': min(depth, max_depth),
            'replies': build_comment_tree(comment.replies.all(), depth + 1, max_depth),
        }
        comment_tree.append(node)
    return comment_tree


def viewPost(request, pk, parent_comment_id=None):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent=None)  # Only fetch top-level comments
    comment_tree = build_comment_tree(comments)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form = form.save(commit=False)
            form.post = post
            form.author = request.user.profile
            form.username = request.user.username
            form.fname = request.user.first_name
            form.lname = request.user.last_name
            # Adds reply to comment if there is a parent_comment_id in the URL pattern
            if parent_comment_id:
                form.parent = Comment.objects.get(id=parent_comment_id)

            form.save()
            return redirect('view-post', pk=post.pk)  # Redirect after POST
        else:
            return redirect(request.GET['next'] if 'next' in request.GET else 'list-posts')

    return render(request, 'forum/view_post.html', {'post':post, 'comments': comments, 'comment_tree':comment_tree, 'form': form})

def editPost(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST' and post.username == request.user.username:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(request.GET['next'] if 'next' in request.GET else 'view-post', pk=pk)
        
        else:
            return redirect(request.GET['next'] if 'next' in request.GET else 'view-post', pk=pk)
    return render(request, 'forum/create_forum_post.html', {"post":post, "form":form})

@csrf_protect
def updateComment(request, comment_id):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        edited_text = data.get('edited_text', '')

        # Update the comment in the database
        comment = Comment.objects.get(id=comment_id)
        comment.text = edited_text
        comment.save()

        return JsonResponse({'message': 'Comment updated successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)

# NOTE: Might not need this view. Leaving it here for now until other possible solution can be fulfilled.
# def editComment(request, pk):
#     comment = get_object_or_404(Comment, id=pk)
#     form = CommentForm(instance=comment)

#     if request.method == 'POST' and comment.username == request.user.username:
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect(request.GET['next'] if 'next' in request.GET else 'view-post', pk=pk)
#         else:
#             return redirect(request.GET['next'] if 'next' in request.GET else 'view-post', pk=pk)
#     return render(request, 'forum/edit_comment.html', {'comment':comment, 'form':form})