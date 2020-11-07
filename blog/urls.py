from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('<int:post_id>/<str:slug>', views.blog_post, name='blog_post'),
    path('blog_user_posts/<str:username>/', views.blog_user_posts, name='blog_user_posts'),
    path('blog_user_rated/<str:username>/', views.blog_user_rated, name='blog_user_rated'),
    path('blog_new_post/<str:username>/', views.blog_new_post, name='blog_new_post'),
    path('blog_edit_post/<str:username>/<int:post_id>', views.blog_edit_post, name='blog_edit_post'),
    path('blog_delete_post/<str:username>/<int:post_id>', views.blog_delete_post, name='blog_delete_post'),
    path('up_vote/<int:user_id>/<int:post_id>', views.up_vote, name='up_vote'),
    path('down_vote/<int:user_id>/<int:post_id>', views.down_vote, name='down_vote'),
    path('blog_posts_from', views.blog_posts_from, name='blog_posts_from'),
    path('write_post_comment', views.write_post_comment, name='write_post_comment'),
    path('edit_post_comment/<int:comment_id>', views.edit_post_comment, name='edit_post_comment'),
    path('delete_post_comment/<int:comment_id>', views.delete_post_comment, name='delete_post_comment')

]