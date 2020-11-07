from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from blog.models import Post, PostComment, Vote
from datetime import datetime, timedelta
from slugify import slugify
from textwrap import shorten


#blog functionality
def blog_home(request):
    all_posts = Post.objects.all().order_by('id')
    pages = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    all_posts = pages.get_page(page_number)
    time_range = 'All Time'
    context = {'all_posts': all_posts, 'time_range': time_range}
    return render(request, 'blog/blog_home.html', context)


def blog_user_posts(request, username):
    all_posts = Post.objects.filter(author=username).order_by('id')
    pages = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    all_posts = pages.get_page(page_number)
    context = {'all_posts': all_posts, 'username': username}
    return render(request, 'blog/blog_user_posts.html', context)


def blog_user_rated(request, username):
    user = request.user
    votes = Vote.objects.filter(user=user, content='up')
    votes = votes.values_list('post', flat=True)
    all_posts = Post.objects.filter(id__in=votes).order_by('id')
    pages = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    all_posts = pages.get_page(page_number)
    context = {'all_posts': all_posts}
    return render(request, 'blog/blog_user_rated.html', context)


def blog_posts_from(request):
    time_range = request.GET.get('time_range')
    if time_range == 'hour':
        time_range = datetime.now() - timedelta(hours=1)
        human_time_range = 'Now'
    elif time_range == 'day':
        time_range = datetime.now() - timedelta(days=1)
        human_time_range = 'Today'
    elif time_range == 'week':
        time_range = datetime.now() - timedelta(days=7)
        human_time_range = 'This Week'
    elif time_range == 'month':
        time_range = datetime.now() - timedelta(weeks=4)
        human_time_range = 'This Month'
    elif time_range == 'year':
        time_range = datetime.now() - timedelta(weeks=52)
        human_time_range = 'This Year'
    else:
        return blog_home(request)
    all_posts = Post.objects.filter(time_stamp__gte=time_range)
    pages = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    all_posts = pages.get_page(page_number)
    context = {'all_posts': all_posts, 'time_range': human_time_range}
    return render(request, 'blog/blog_home.html', context)


#posts API
def blog_post(request, post_id, slug):
    post = Post.objects.get(id=post_id)
    post.views = post.views + 1
    post.save()
    comments = PostComment.objects.filter(post=post)
    context = {'post': post, 'comments': comments}
    return render(request, 'blog/blog_post.html', context)


def blog_new_post(request, username):
    if request.method == 'POST':
        title = request.POST['title']
        author = username
        content = request.POST['content']
        source = request.POST['source']
        slug = slugify(shorten(title.lower(), width=50), separator='_')
        if len(title) < 5 or len(content) < 5 or len(source) < 5:
            messages.error(request, "Enter valid data in form.")
        else:
            post_obj = Post(title=title, author=author, content=content, slug=slug, source=source)
            post_obj.save()
            messages.success(request, "Your post have been created.")
            return redirect(f'/blog/blog_user_posts/{username}/')
    return render(request, 'blog/blog_new_post.html')


def blog_edit_post(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        new_title = request.POST['title']
        new_content = request.POST['content']
        new_source = request.POST['source']
        if len(new_title) < 5 or len(new_content) < 5 or len(new_source) < 5:
            messages.error(request, "Enter valid data in form.")
        else:
            post = Post.objects.get(pk=post_id)
            post.title = new_title
            post.content = new_content
            post.save()
            messages.success(request, "Post has been edited.")
            return redirect(f'/blog/blog_user_posts/{username}/')
    context = {'post': post}
    return render(request, 'blog/blog_edit_post.html', context)


def blog_delete_post(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    messages.success(request, "Post has been deleted.")
    return redirect(f'/blog/blog_user_posts/{username}/')


#comments API
def write_post_comment(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        post.comments = post.comments + 1
        post.save()

        user = request.user
        content = request.POST.get('content')
        comment = PostComment(post=post, user=user, content=content)
        comment.save()
        messages.success(request, "You comment has been posted.")

        return redirect(f'/blog/{post.id}/{post.slug}')


def edit_post_comment(request, comment_id):
    new_content = request.POST['content']
    comment = PostComment.objects.get(pk=comment_id)
    post = comment.post
    comment.content = new_content
    comment.save()
    messages.success(request, "Comment has been edited.")
    return redirect(f'/blog/{post.id}/{post.slug}')


def delete_post_comment(request, comment_id):
    comment = PostComment.objects.get(pk=comment_id)
    comment.delete()
    post = comment.post
    post.comments = post.comments - 1
    post.save()
    messages.success(request, "Comment has been deleted.")
    return redirect(f'/blog/{post.id}/{post.slug}')


#votes API
def up_vote(request, user_id, post_id):
    user = User.objects.get(pk=user_id)
    post = Post.objects.get(pk=post_id)
    vote = Vote.objects.filter(user=user, post=post).first()
    if vote:
        if vote.content == 'up':
            messages.error(request, "You have already upvoted this post.")
            return redirect(f'/blog/{post.id}/{post.slug}')
        else:
            vote.content = 'up'
            vote.save()
            post.votes_up = post.votes_up + 1
            post.votes_down = post.votes_down - 1
            post.save()
            messages.success(request, "Your up vote has been added to the post.")
            return redirect(f'/blog/{post.id}/{post.slug}')
    else:
        vote = Vote(user=user, post=post, content='up')
        vote.save()
        post.votes_up = post.votes_up + 1
        post.save()
        messages.success(request, "Your up vote has been added to the post.")
        return redirect(f'/blog/{post.id}/{post.slug}')


def down_vote(request, user_id, post_id):
    user = User.objects.get(pk=user_id)
    post = Post.objects.get(pk=post_id)
    vote = Vote.objects.filter(user=user, post=post).first()
    if vote:
        if vote.content == 'down':
            messages.error(request, "You have already downvoted this post.")
            return redirect(f'/blog/{post.id}/{post.slug}')
        else:
            vote.content = 'down'
            vote.save()
            post.votes_up = post.votes_up - 1
            post.votes_down = post.votes_down + 1
            post.save()
            messages.success(request, "Your down vote has been added to the post.")
            return redirect(f'/blog/{post.id}/{post.slug}')
    else:
        vote = Vote(user=user, post=post, content='down')
        vote.save()
        post.votes_down = post.votes_down + 1
        post.save()
        messages.success(request, "Your down vote has been added to the post.")
        return redirect(f'/blog/{post.id}/{post.slug}')
