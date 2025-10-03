from django.contrib import admin
from .models import Petition, Vote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_title', 'created_by', 'created_at', 'vote_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'movie_title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'petition__title']
