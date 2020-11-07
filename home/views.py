from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from home.models import Contact
from blog.models import Post


# main functionality
def home(request):
    most_discussed = Post.objects.all().order_by('-comments')[:3]
    most_viewed = Post.objects.all().order_by('-views')[:3]
    most_rated = sorted(Post.objects.all(), key=lambda x: x.get_rating(), reverse=True)[:3]
    context = {'most_rated': most_rated,
               'most_viewed': most_viewed,
               'most_discussed': most_discussed
               }
    return render(request, 'home/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 7 or len(phone) < 10 or len(content) < 10:
            messages.error(request, "Enter valid data in form.")
        else:
            contact_obj = Contact(name=name, email=email, phone=phone, content=content)
            contact_obj.save()
            messages.success(request, "Your message have been sent. We will contact you soon.")

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) == 0:
        messages.warning(request, "Search query is empty.")
        all_posts = Post.objects.none()
    elif len(query) > 100:
        messages.warning(request, "Search query has too many characters.")
        all_posts = Post.objects.none()
    else:
        all_posts = Post.objects.filter(title__icontains=query).order_by('id') | \
                    Post.objects.filter(content__icontains=query).order_by('id') | \
                    Post.objects.filter(author__icontains=query).order_by('id') | \
                    Post.objects.filter(source__icontains=query).order_by('id')

    pages = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    all_posts = pages.get_page(page_number)
    context = {'all_posts': all_posts, 'query': query}
    return render(request, 'home/search.html', context)


# authentication
def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not username.isalnum() or not username.islower():
            messages.error(request, "Username should only contain lowercase letters and numbers.")
            return redirect(request.META['HTTP_REFERER'])
        elif len(username) > 15:
            messages.warning(request, "Username should be under 15 characters.")
            return redirect(request.META['HTTP_REFERER'])
        elif password1 != password2:
            messages.error(request, "Passwords don't match. Try again.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account has been created successfully.")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("404 - Not Found")


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Wrong username or password. Try again.")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("404 - Not Found")


def log_out(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('/')
