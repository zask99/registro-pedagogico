from django.contrib import admin
from .models import task

@admin.register(task)
class taskadmin(admin.ModelAdmin):
    list_display=['title','created']