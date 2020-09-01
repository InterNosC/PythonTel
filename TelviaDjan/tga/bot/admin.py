from django.contrib import admin

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')

@admin.register(Message)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')
