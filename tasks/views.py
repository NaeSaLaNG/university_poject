"""
Views (ViewSets) для API управления проектами и задачами.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Project, Task
from .serializers import (
    ProjectListSerializer, ProjectDetailSerializer,
    TaskListSerializer, TaskDetailSerializer, TaskCreateUpdateSerializer
)
from .filters import ProjectFilter, TaskFilter


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления проектами.
    
    Предоставляет CRUD операции для проектов:
    - list: получить список проектов
    - create: создать новый проект
    - retrieve: получить детальную информацию о проекте
    - update: обновить проект
    - partial_update: частично обновить проект
    - destroy: удалить проект
    """
    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer

    def perform_create(self, serializer):
        """Автоматически устанавливаем владельца проекта"""
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        method='get',
        operation_description="Получить статистику по проекту",
        responses={200: openapi.Response(
            description="Статистика проекта",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_tasks': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'completed_tasks': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'in_progress_tasks': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'todo_tasks': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'overdue_tasks': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )}
    )
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Получить статистику по проекту"""
        project = self.get_object()
        from django.utils import timezone
        
        stats = {
            'total_tasks': project.tasks.count(),
            'completed_tasks': project.tasks.filter(status='completed').count(),
            'in_progress_tasks': project.tasks.filter(status='in_progress').count(),
            'todo_tasks': project.tasks.filter(status='todo').count(),
            'overdue_tasks': project.tasks.filter(
                deadline__lt=timezone.now()
            ).exclude(status__in=['completed', 'cancelled']).count(),
        }
        return Response(stats)

    @swagger_auto_schema(
        method='get',
        operation_description="Получить задачи проекта",
        responses={200: TaskListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Получить все задачи проекта"""
        project = self.get_object()
        tasks = project.tasks.all()
        
        # Применяем фильтры
        task_filter = TaskFilter(request.GET, queryset=tasks)
        page = self.paginate_queryset(task_filter.qs)
        
        if page is not None:
            serializer = TaskListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления задачами.
    
    Предоставляет CRUD операции для задач с расширенной фильтрацией:
    - list: получить список задач
    - create: создать новую задачу
    - retrieve: получить детальную информацию о задаче
    - update: обновить задачу
    - partial_update: частично обновить задачу
    - destroy: удалить задачу
    
    Фильтрация:
    - по статусу (status)
    - по приоритету (priority)
    - по проекту (project)
    - по исполнителю (assignee)
    - по дате создания (created_after, created_before)
    - по дедлайну (deadline_after, deadline_before)
    - просроченные задачи (is_overdue=true)
    - без исполнителя (no_assignee=true)
    """
    queryset = Task.objects.select_related('project', 'assignee', 'creator').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at', 'updated_at', 'deadline', 'status']
    ordering = ['-priority', '-created_at']

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskListSerializer

    def perform_create(self, serializer):
        """Автоматически устанавливаем создателя задачи"""
        serializer.save(creator=self.request.user)

    @swagger_auto_schema(
        method='post',
        operation_description="Изменить статус задачи",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['status'],
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['todo', 'in_progress', 'review', 'completed', 'cancelled']
                )
            }
        ),
        responses={200: TaskDetailSerializer()}
    )
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Изменить статус задачи"""
        task = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {'error': 'Недопустимый статус'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        task.save()
        
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        operation_description="Назначить задачу пользователю",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['assignee_id'],
            properties={
                'assignee_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: TaskDetailSerializer()}
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Назначить задачу пользователю"""
        task = self.get_object()
        assignee_id = request.data.get('assignee_id')
        
        if not assignee_id:
            return Response(
                {'error': 'Требуется assignee_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth.models import User
        try:
            assignee = User.objects.get(id=assignee_id)
            task.assignee = assignee
            task.save()
            
            serializer = TaskDetailSerializer(task)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        method='get',
        operation_description="Получить задачи текущего пользователя",
        responses={200: TaskListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Получить задачи, назначенные текущему пользователю"""
        tasks = self.queryset.filter(assignee=request.user)
        
        # Применяем фильтры
        task_filter = TaskFilter(request.GET, queryset=tasks)
        page = self.paginate_queryset(task_filter.qs)
        
        if page is not None:
            serializer = TaskListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

