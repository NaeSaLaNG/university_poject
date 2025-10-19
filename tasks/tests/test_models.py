"""
Тесты для моделей Project и Task.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from tasks.models import Project, Task


@pytest.mark.django_db
class TestProjectModel:
    """Тесты модели Project"""
    
    def test_create_project(self, user):
        """Тест создания проекта"""
        project = Project.objects.create(
            name='New Project',
            description='Project description',
            owner=user
        )
        assert project.name == 'New Project'
        assert project.owner == user
        assert project.is_active is True
        assert project.tasks_count == 0
    
    def test_project_str(self, project):
        """Тест строкового представления проекта"""
        assert str(project) == project.name
    
    def test_tasks_count(self, project, user):
        """Тест подсчета задач в проекте"""
        Task.objects.create(
            title='Task 1',
            project=project,
            creator=user
        )
        Task.objects.create(
            title='Task 2',
            project=project,
            creator=user
        )
        assert project.tasks_count == 2
    
    def test_completed_tasks_count(self, project, user):
        """Тест подсчета завершенных задач"""
        Task.objects.create(
            title='Task 1',
            project=project,
            creator=user,
            status='completed'
        )
        Task.objects.create(
            title='Task 2',
            project=project,
            creator=user,
            status='todo'
        )
        assert project.completed_tasks_count == 1


@pytest.mark.django_db
class TestTaskModel:
    """Тесты модели Task"""
    
    def test_create_task(self, project, user):
        """Тест создания задачи"""
        task = Task.objects.create(
            title='New Task',
            description='Task description',
            project=project,
            creator=user,
            status='todo',
            priority=2
        )
        assert task.title == 'New Task'
        assert task.project == project
        assert task.creator == user
        assert task.status == 'todo'
        assert task.priority == 2
    
    def test_task_str(self, task):
        """Тест строкового представления задачи"""
        expected = f"{task.title} ({task.get_status_display()})"
        assert str(task) == expected
    
    def test_task_auto_completed_at(self, task):
        """Тест автоматической установки даты завершения"""
        assert task.completed_at is None
        task.status = 'completed'
        task.save()
        assert task.completed_at is not None
    
    def test_task_clear_completed_at(self, task):
        """Тест очистки даты завершения при изменении статуса"""
        task.status = 'completed'
        task.save()
        assert task.completed_at is not None
        
        task.status = 'in_progress'
        task.save()
        assert task.completed_at is None
    
    def test_task_is_overdue(self, task):
        """Тест проверки просроченной задачи"""
        # Задача без дедлайна не просрочена
        assert task.is_overdue is False
        
        # Задача с дедлайном в будущем не просрочена
        task.deadline = timezone.now() + timedelta(days=1)
        task.save()
        assert task.is_overdue is False
        
        # Задача с дедлайном в прошлом просрочена
        task.deadline = timezone.now() - timedelta(days=1)
        task.save()
        assert task.is_overdue is True
        
        # Завершенная задача не просрочена
        task.status = 'completed'
        task.save()
        assert task.is_overdue is False

