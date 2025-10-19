"""
Тесты API для задач.
"""
import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from tasks.models import Task


@pytest.mark.django_db
class TestTaskAPI:
    """Тесты API задач"""
    
    def test_list_tasks(self, authenticated_client, task):
        """Тест получения списка задач"""
        url = reverse('tasks:task-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_task(self, authenticated_client, project, user):
        """Тест создания задачи"""
        url = reverse('tasks:task-list')
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'project': project.id,
            'status': 'todo',
            'priority': 3
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Task'
        
        # Проверяем, что задача создана в базе
        assert Task.objects.count() == 1
        task = Task.objects.first()
        assert task.creator == user
    
    def test_retrieve_task(self, authenticated_client, task):
        """Тест получения деталей задачи"""
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == task.title
        assert 'project_detail' in response.data
    
    def test_update_task(self, authenticated_client, task):
        """Тест обновления задачи"""
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        data = {'title': 'Updated Task Title', 'priority': 4}
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Task Title'
        
        task.refresh_from_db()
        assert task.title == 'Updated Task Title'
        assert task.priority == 4
    
    def test_delete_task(self, authenticated_client, task):
        """Тест удаления задачи"""
        url = reverse('tasks:task-detail', kwargs={'pk': task.id})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0
    
    def test_change_status(self, authenticated_client, task):
        """Тест изменения статуса задачи"""
        url = reverse('tasks:task-change-status', kwargs={'pk': task.id})
        data = {'status': 'in_progress'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'in_progress'
        
        task.refresh_from_db()
        assert task.status == 'in_progress'
    
    def test_assign_task(self, authenticated_client, task, another_user):
        """Тест назначения задачи пользователю"""
        url = reverse('tasks:task-assign', kwargs={'pk': task.id})
        data = {'assignee_id': another_user.id}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['assignee']['id'] == another_user.id
        
        task.refresh_from_db()
        assert task.assignee == another_user
    
    def test_my_tasks(self, authenticated_client, project, user, another_user):
        """Тест получения задач текущего пользователя"""
        # Создаем задачи для разных пользователей
        Task.objects.create(
            title='My Task',
            project=project,
            creator=user,
            assignee=user
        )
        Task.objects.create(
            title='Another Task',
            project=project,
            creator=user,
            assignee=another_user
        )
        
        url = reverse('tasks:task-my-tasks')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'My Task'
    
    def test_filter_tasks_by_status(self, authenticated_client, project, user):
        """Тест фильтрации задач по статусу"""
        Task.objects.create(
            title='Todo Task',
            project=project,
            creator=user,
            status='todo'
        )
        Task.objects.create(
            title='Completed Task',
            project=project,
            creator=user,
            status='completed'
        )
        
        url = reverse('tasks:task-list')
        response = authenticated_client.get(url, {'status': 'todo'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['status'] == 'todo'
    
    def test_filter_tasks_by_priority(self, authenticated_client, project, user):
        """Тест фильтрации задач по приоритету"""
        Task.objects.create(
            title='High Priority Task',
            project=project,
            creator=user,
            priority=4
        )
        Task.objects.create(
            title='Low Priority Task',
            project=project,
            creator=user,
            priority=1
        )
        
        url = reverse('tasks:task-list')
        response = authenticated_client.get(url, {'priority': '4'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['priority'] == 4
    
    def test_filter_overdue_tasks(self, authenticated_client, project, user):
        """Тест фильтрации просроченных задач"""
        # Просроченная задача
        Task.objects.create(
            title='Overdue Task',
            project=project,
            creator=user,
            deadline=timezone.now() - timedelta(days=1)
        )
        # Задача в срок
        Task.objects.create(
            title='Future Task',
            project=project,
            creator=user,
            deadline=timezone.now() + timedelta(days=1)
        )
        
        url = reverse('tasks:task-list')
        response = authenticated_client.get(url, {'is_overdue': 'true'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Overdue Task'
    
    def test_search_tasks(self, authenticated_client, project, user):
        """Тест поиска задач"""
        Task.objects.create(
            title='Django Development',
            description='Backend work',
            project=project,
            creator=user
        )
        Task.objects.create(
            title='React Development',
            description='Frontend work',
            project=project,
            creator=user
        )
        
        url = reverse('tasks:task-list')
        response = authenticated_client.get(url, {'search': 'Backend'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Django Development'

