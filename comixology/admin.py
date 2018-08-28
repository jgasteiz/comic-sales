from django.contrib import admin

from . import models


class SaleAdmin(admin.ModelAdmin):
    list_display = ['platform_id', 'title', 'date_end', 'num_items', 'url']
    search_fields = ['title']


admin.site.register(models.Sale, SaleAdmin)
