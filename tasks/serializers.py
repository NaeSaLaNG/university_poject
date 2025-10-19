"""
Сериализаторы для API проектов и задач.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Task


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProjectListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка проектов (краткая информация)"""
    owner = UserSerializer(read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)
    completed_tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'owner', 
            'is_active', 'tasks_count', 'completed_tasks_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Подробный сериализатор проекта с задачами"""
    owner = UserSerializer(read_only=True)
    tasks_count = serializers.IntegerField(read_only=True)
    completed_tasks_count = serializers.IntegerField(read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'owner', 
            'is_active', 'tasks_count', 'completed_tasks_count',
            'tasks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_tasks(self, obj):
        """Получить краткую информацию о задачах проекта"""
        tasks = obj.tasks.all()[:10]  # Ограничиваем 10 задачами
        return TaskListSerializer(tasks, many=True).data


class TaskListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка задач (краткая информация)"""
    assignee = UserSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'project', 'project_name',
            'assignee', 'creator', 'status', 'status_display',
            'priority', 'priority_display', 'deadline', 
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    """Подробный сериализатор задачи"""
    assignee = UserSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    project_detail = ProjectListSerializer(source='project', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_detail',
            'assignee', 'assignee_id', 'creator', 
            'status', 'status_display', 'priority', 'priority_display',
            'deadline', 'is_overdue', 
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at', 'completed_at']

    def validate_deadline(self, value):
        """Проверка, что дедлайн не в прошлом при создании"""
        if value:
            from django.utils import timezone
            if self.instance is None and value < timezone.now():
                raise serializers.ValidationError(
                    "Дедлайн не может быть в прошлом."
                )
        return value

    def validate(self, data):
        """Дополнительная валидация"""
        # Проверяем, что пользователь имеет доступ к проекту
        project = data.get('project', self.instance.project if self.instance else None)
        request = self.context.get('request')
        
        if project and request:
            # Владелец проекта может делать все
            if project.owner != request.user:
                # Можно добавить дополнительные проверки прав
                pass
        
        return data


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления задачи"""
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project',
            'assignee', 'status', 'priority', 'deadline'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Создание задачи с автоматической установкой создателя"""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

