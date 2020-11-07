from django.contrib import admin
from blog.models import Post, PostComment, Vote


# Register your models here.
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Vote)


