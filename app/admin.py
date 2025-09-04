from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EnvironmentalData, ChatHistory, Post, Comment

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class EnvironmentalDataAdmin(admin.ModelAdmin):
    list_display = ('category', 'keyword', 'question', 'source', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('keyword', 'question', 'answer')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('category', 'keyword')
        }),
        ('Contenu', {
            'fields': ('question', 'answer')
        }),
        ('Métadonnées', {
            'fields': ('source', 'created_at'),
            'classes': ('collapse',)
        }),
    )

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user_message', 'category', 'timestamp')
    list_filter = ('category', 'timestamp')
    search_fields = ('user_message', 'bot_response', 'session_id')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('Conversation', {
            'fields': ('session_id', 'user_message', 'bot_response')
        }),
        ('Métadonnées', {
            'fields': ('category', 'timestamp'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 50

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'likes_count')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'likes_count')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username', 'post__title')
    readonly_fields = ('created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EnvironmentalData, EnvironmentalDataAdmin)
admin.site.register(ChatHistory, ChatHistoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
