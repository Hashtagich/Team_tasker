from django.contrib import admin
from .models import Task


# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'status',
        'author',
        'implementer',
        'datetime_start',
        'datetime_finish_plan',
        'datetime_finish_fact',
        'datetime_update',
        'datetime_create',
        'description',
        'id'
    )

    search_fields = (
        'name',
        'status',
        'author',
        'implementer',
        'datetime_start',
        'datetime_finish_plan',
        'datetime_finish_fact',
        'datetime_create'
    )

    list_filter = (
        'status',
        'name',
        'datetime_start'
    )
