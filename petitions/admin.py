from django.contrib import admin
from .models import Petition, PetitionVote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'title', 'proposer', 'is_open', 'created_at')
    search_fields = ('movie_title', 'title', 'description')

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'value', 'created_at')
    list_filter = ('value',)
