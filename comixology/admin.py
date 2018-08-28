from django.contrib import admin

from . import models


class SaleAdmin(admin.ModelAdmin):
    ordering = ['-created_at', 'title']
    list_display = ['platform_id', 'title', 'date_end', 'num_items', 'url', 'created_at']
    search_fields = ['title']


admin.site.register(models.Sale, SaleAdmin)
