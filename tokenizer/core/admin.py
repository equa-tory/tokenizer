from django.contrib import admin
from .models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'date', 'small_preview')
    list_editable = ('title', 'small_preview')
    search_fields = ('number', 'title', 'description')