"""
Фильтры для API задач и проектов.
"""
from django_filters import rest_framework as filters
from .models import Task, Project


class ProjectFilter(filters.FilterSet):
    """Фильтры для проектов"""
    name = filters.CharFilter(lookup_expr='icontains', label='Название содержит')
    owner = filters.NumberFilter(field_name='owner__id', label='ID владельца')
    is_active = filters.BooleanFilter(label='Активен')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte', label='Создан после')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte', label='Создан до')

    class Meta:
        model = Project
        fields = ['name', 'owner', 'is_active', 'created_after', 'created_before']


class TaskFilter(filters.FilterSet):
    """Фильтры для задач"""
    title = filters.CharFilter(lookup_expr='icontains', label='Название содержит')
    status = filters.MultipleChoiceFilter(
        choices=Task.STATUS_CHOICES,
        label='Статус (можно несколько)'
    )
    priority = filters.MultipleChoiceFilter(
        choices=Task.PRIORITY_CHOICES,
        label='Приоритет (можно несколько)'
    )
    project = filters.NumberFilter(field_name='project__id', label='ID проекта')
    project_name = filters.CharFilter(
        field_name='project__name', 
        lookup_expr='icontains',
        label='Название проекта содержит'
    )
    assignee = filters.NumberFilter(field_name='assignee__id', label='ID исполнителя')
    creator = filters.NumberFilter(field_name='creator__id', label='ID создателя')
    
    # Фильтры по датам
    created_after = filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte',
        label='Создана после'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte',
        label='Создана до'
    )
    deadline_after = filters.DateTimeFilter(
        field_name='deadline', 
        lookup_expr='gte',
        label='Дедлайн после'
    )
    deadline_before = filters.DateTimeFilter(
        field_name='deadline', 
        lookup_expr='lte',
        label='Дедлайн до'
    )
    
    # Специальные фильтры
    is_overdue = filters.BooleanFilter(
        method='filter_overdue',
        label='Просроченные задачи'
    )
    no_assignee = filters.BooleanFilter(
        method='filter_no_assignee',
        label='Без исполнителя'
    )

    class Meta:
        model = Task
        fields = [
            'title', 'status', 'priority', 'project', 
            'assignee', 'creator', 'project_name'
        ]

    def filter_overdue(self, queryset, name, value):
        """Фильтр просроченных задач"""
        if value:
            from django.utils import timezone
            return queryset.filter(
                deadline__lt=timezone.now()
            ).exclude(
                status__in=['completed', 'cancelled']
            )
        return queryset

    def filter_no_assignee(self, queryset, name, value):
        """Фильтр задач без исполнителя"""
        if value:
            return queryset.filter(assignee__isnull=True)
        return queryset

