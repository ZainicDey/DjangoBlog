from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('home/', views.home, name = 'home'),
    path('sign-up/', views.signup, name = 'sign_up'),
    path('create-post/', views.post, name='post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('comment-post/<int:post_id>/', views.comment_post, name='comment_post'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]
