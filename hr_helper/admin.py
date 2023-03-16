from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib import admin
from .models import Opis

@admin.register(Opis)
class CVAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    search_fields = ('user__username', 'title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
