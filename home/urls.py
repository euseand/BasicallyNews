from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('signup', views.sign_up, name='signup'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout')

]