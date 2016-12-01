from django.contrib import admin

# Register your models here.
from .models import Post, UserModel

admin.site.register(Post)
admin.site.register(UserModel)
