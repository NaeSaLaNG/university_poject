"""
Административная панель Django для управления проектами и задачами.
"""
from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Администрирование проектов"""
    list_display = ['name', 'owner', 'is_active', 'tasks_count', 'created_at']
    list_filter = ['is_active', 'created_at', 'owner']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'tasks_count', 'completed_tasks_count']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'owner', 'is_active')
        }),
        ('Статистика', {
            'fields': ('tasks_count', 'completed_tasks_count')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Администрирование задач"""
    list_display = [
        'title', 'project', 'assignee', 'status', 
        'priority', 'deadline', 'is_overdue', 'created_at'
    ]
    list_filter = ['status', 'priority', 'project', 'created_at', 'deadline']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'is_overdue']
    autocomplete_fields = ['project', 'assignee', 'creator']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'project')
        }),
        ('Назначение', {
            'fields': ('creator', 'assignee')
        }),
        ('Параметры', {
            'fields': ('status', 'priority', 'deadline')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        """Отображение просроченных задач"""
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Просрочена'

