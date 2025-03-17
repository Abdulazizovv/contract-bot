from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'username', 'is_checked', 'created_at', 'updated_at')
    search_fields = ('user_id', 'full_name', 'username')
    list_filter = ('is_checked', 'created_at', 'updated_at')
    list_per_page = 20
    list_display_links = ('user_id', 'full_name', 'username')


admin.site.register(BotUser, BotUserAdmin)