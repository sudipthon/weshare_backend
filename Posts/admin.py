from django.contrib import admin
from .models import *

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Number of extra "empty" forms
class ImageInline(admin.TabularInline):
    model = Image
    extra = 0  # Number of extra "empty" forms

class ReportsInline(admin.TabularInline):
    model = Reports
    extra = 0  # Number of extra "empty" forms

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline,ImageInline,ReportsInline]
    list_filter = ('post_type','flag')
    list_display = ('__str__', 'author','post_type','report_count','flag')
    
    def report_count(self, obj):
        return obj.post_reports.count()

    
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
    