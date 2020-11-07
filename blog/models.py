from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=15)
    content = models.TextField()
    slug = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    votes_up = models.IntegerField(default=0)
    votes_down = models.IntegerField(default=0)

    def __str__(self):
        return self.title + ' posted by ' + self.author + ' - ' + self.time_stamp.strftime("%d/%m/%Y, %H:%M:%S")

    def get_rating(self):
        return (self.votes_up + self.votes_down) * (self.votes_up - self.votes_down)

    def get_date(self):
        return format_date(self)


class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment "' + self.content[0:19] + '..." posted by ' + self.user.username + ' - ' + \
               self.time_stamp.strftime("%d/%m/%Y, %H:%M:%S")

    def get_date(self):
        return format_date(self)


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=4)

    def __str__(self):
        return 'Vote ' + self.content + ' by ' + self.user.username + ' - post ' + self.post.title


def format_date(self):
    time = datetime.now()
    if self.time_stamp.minute == time.minute and self.time_stamp.hour == time.hour and self.time_stamp.day == time.day:
        if (time.minute - self.time_stamp.minute) % 10 == 1:
            return str(time.second - self.time_stamp.second) + " second ago"
        else:
            return str(time.second - self.time_stamp.second) + " seconds ago"
    elif self.time_stamp.hour == time.hour and self.time_stamp.day == time.day:
        if (time.minute - self.time_stamp.minute) % 10 == 1:
            return str(time.minute - self.time_stamp.minute) + " minute ago"
        else:
            return str(time.minute - self.time_stamp.minute) + " minutes ago"
    elif self.time_stamp.day == time.day:
        if (time.hour - self.time_stamp.hour) % 10 == 1:
            return str(time.hour - self.time_stamp.hour) + " hour ago"
        else:
            return str(time.hour - self.time_stamp.hour) + " hours ago"
    elif self.time_stamp.month == time.month:
        if (time.day - self.time_stamp.day) % 10 == 1:
            return str(time.day - self.time_stamp.day) + " day ago"
        else:
            return str(time.day - self.time_stamp.day) + " days ago"
    elif self.time_stamp.year == time.year:
        if (time.month - self.time_stamp.month) % 10 == 1:
            return str(time.month - self.time_stamp.month) + " month ago"
        else:
            return str(time.month - self.time_stamp.month) + " months ago"
    elif (time.year - self.time_stamp.year) % 10 == 1:
        return str(time.year - self.time_stamp.year) + " year ago"
    else:
        return str(time.year - self.time_stamp.year) + " years ago"