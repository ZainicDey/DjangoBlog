from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,PostForm, CommentForm
from . import models
from django.contrib import messages
from django.http import HttpResponseNotFound
# Create your views here.
@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = models.Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
        return redirect('/home')
    posts = models.Post.objects.annotate(
    likes_count=Count('likes', distinct=True),
    comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')

    return render(request, 'home.html', {'posts': posts})

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if models.User.objects.filter(email=email).exists():
                form.add_error('email', "An account with this email already exists.")
            else:
                user = form.save()
                login(request, user)
                return redirect('/home')
    elif request.user.is_authenticated:
        messages.info(request, "You need to log out to create a new account.")  
        return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})

class CustomLoginView(LoginView):
    def dispatch(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request)
@login_required(login_url='/home') 
def post(request):
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.author = request.user
            post_instance.save()
            return redirect('/home')
    else:
        form = PostForm()
        return render(request, 'post.html', {'form': form})

@login_required(login_url='/login')
def like_post(request, post_id):
    post = models.Post.objects.filter(id=post_id).first()
    existing_like = models.Like.objects.filter(user=request.user, post=post).first()

    if existing_like:
        existing_like.delete()
    else:
        models.Like.objects.create(user=request.user, post=post)

    return redirect('home')

@login_required(login_url='/login')
def comment_post(request, post_id):
    post = models.Post.objects.filter(id=post_id).first()   
    if not post:
        return HttpResponseNotFound("Post not found")

    comments = models.Comment.objects.filter(post=post)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user 
            comment.post = post
            comment.updated_at = comment.created_at
            comment.save()
            return redirect('comment_post', post_id=post.id)
    else:
        form = CommentForm() 

    return render(request, 'comments.html', {
        "post": post,
        "comments": comments,
        "form": form,
    })

@login_required(login_url='/login')
def comment_delete(request, comment_id):
    comment = models.Comment.objects.filter(id=comment_id).first()

    if request.user == comment.author:
        comment.delete()
    
    return redirect('comment_post', post_id=comment.post.id)

@login_required(login_url='/login')
def edit_comment(request, comment_id):
    comment = models.Comment.objects.filter(id=comment_id).first()
    current_content = comment.content
    print(comment.content)
    if not comment:
        return HttpResponseNotFound('Comment not found')

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment) 
        if form.is_valid():
            new_content = form.cleaned_data.get('content').strip() 
            if new_content != current_content:
                form.save()
                print("Comment updated successfully.")
            else:
                print("No changes detected. Comment not updated.")
            return redirect('comment_post', comment.post.id)  
    else:
        form = CommentForm(instance=comment)  

    return render(request, 'edit_comment.html', {'form': form})
