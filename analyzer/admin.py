from django.contrib import admin
from .models import Conversation


@admin.register(Conversation)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")

