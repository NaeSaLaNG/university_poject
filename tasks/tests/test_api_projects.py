"""
Тесты API для проектов.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from tasks.models import Project


@pytest.mark.django_db
class TestProjectAPI:
    """Тесты API проектов"""
    
    def test_list_projects(self, authenticated_client, project):
        """Тест получения списка проектов"""
        url = reverse('tasks:project-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_project(self, authenticated_client, user):
        """Тест создания проекта"""
        url = reverse('tasks:project-list')
        data = {
            'name': 'New Project',
            'description': 'New project description',
            'is_active': True
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Project'
        assert response.data['owner']['id'] == user.id
        
        # Проверяем, что проект создан в базе
        assert Project.objects.count() == 1
    
    def test_retrieve_project(self, authenticated_client, project):
        """Тест получения деталей проекта"""
        url = reverse('tasks:project-detail', kwargs={'pk': project.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == project.name
        assert 'tasks' in response.data
    
    def test_update_project(self, authenticated_client, project):
        """Тест обновления проекта"""
        url = reverse('tasks:project-detail', kwargs={'pk': project.id})
        data = {'name': 'Updated Project Name'}
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Project Name'
        
        project.refresh_from_db()
        assert project.name == 'Updated Project Name'
    
    def test_delete_project(self, authenticated_client, project):
        """Тест удаления проекта"""
        url = reverse('tasks:project-detail', kwargs={'pk': project.id})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Project.objects.count() == 0
    
    def test_project_statistics(self, authenticated_client, project, user):
        """Тест получения статистики проекта"""
        from tasks.models import Task
        
        # Создаем несколько задач
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
            status='in_progress'
        )
        Task.objects.create(
            title='Task 3',
            project=project,
            creator=user,
            status='todo'
        )
        
        url = reverse('tasks:project-statistics', kwargs={'pk': project.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_tasks'] == 3
        assert response.data['completed_tasks'] == 1
        assert response.data['in_progress_tasks'] == 1
        assert response.data['todo_tasks'] == 1
    
    def test_filter_projects_by_name(self, authenticated_client, user):
        """Тест фильтрации проектов по имени"""
        Project.objects.create(name='Alpha Project', owner=user)
        Project.objects.create(name='Beta Project', owner=user)
        
        url = reverse('tasks:project-list')
        response = authenticated_client.get(url, {'name': 'Alpha'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Alpha Project'
    
    def test_search_projects(self, authenticated_client, user):
        """Тест поиска проектов"""
        Project.objects.create(
            name='Django Project', 
            description='Python web framework',
            owner=user
        )
        Project.objects.create(
            name='React Project', 
            description='JavaScript library',
            owner=user
        )
        
        url = reverse('tasks:project-list')
        response = authenticated_client.get(url, {'search': 'Python'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

