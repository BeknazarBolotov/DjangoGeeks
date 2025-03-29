from django.contrib import admin
from posts.models import Post, Category, Tag



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'rate', 'author']
    list_filter = ['rate', 'category']
    list_editable = ['author']

admin.site.register(Category)
admin.site.register(Tag)