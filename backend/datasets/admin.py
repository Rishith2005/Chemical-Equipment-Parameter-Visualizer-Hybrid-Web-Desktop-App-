from django.contrib import admin

from .models import Dataset, DatasetSummary


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "filename", "status", "uploaded_at")
    list_filter = ("status", "uploaded_at")
    search_fields = ("filename", "user__username")


@admin.register(DatasetSummary)
class DatasetSummaryAdmin(admin.ModelAdmin):
    list_display = ("id", "dataset", "user", "generated_at")
    list_filter = ("generated_at",)

# Register your models here.
