from django.contrib import admin
from .models import UserProfile, Movie, Review, Comment, Like

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email')
    search_fields = ('user__username', 'user__email')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_year')
    list_filter = ('genre', 'release_year')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'timestamp')
    list_filter = ('rating', 'timestamp')
    search_fields = ('text', 'movie__title', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('text', 'author__username')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'timestamp')
    list_filter = ('timestamp',)
