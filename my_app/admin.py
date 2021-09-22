from django.contrib import admin
from .models import Search

# Register your models here.


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    readonly_fields = ['created']
    fields = ['search', 'created']
    list_display = ['id', 'search', 'created']
