from django.contrib import admin
from .models import *

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Number of extra "empty" forms
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0  # Number of extra "empty" forms

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline,ImageInline]
    list_filter = ('post_type',)
    list_display = ('__str__', 'time_stamp', 'author','post_type')
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'time_stamp', 'text', 'post')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')

@admin.register(Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('post', 'reason')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    