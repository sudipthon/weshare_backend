from django.contrib import admin

# Register your models here.
from .models import *

class ConversationAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants',)
    list_display = ('id', 'updated_at', 'participants_list')
    search_fields = ('participants__username',)
    
    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    
    participants_list.short_description = "Participants"

class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'author', 'text', 'time_stamp')
    search_fields = ('conversation__id', 'author__username', 'text')
    
    def conversation(self, obj):
        return obj.conversation.id
    
    def author(self, obj):
        return obj.author.username
    
    
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messages, MessagesAdmin)
