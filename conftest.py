"""
Конфигурация pytest и фикстуры для тестирования.
"""
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tasks.models import Project, Task


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return APIClient()


@pytest.fixture
def user(db):
    """Фикстура для создания пользователя"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def another_user(db):
    """Фикстура для создания второго пользователя"""
    return User.objects.create_user(
        username='anotheruser',
        email='another@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Фикстура для аутентифицированного клиента"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def project(user):
    """Фикстура для создания проекта"""
    return Project.objects.create(
        name='Test Project',
        description='Test project description',
        owner=user,
        is_active=True
    )


@pytest.fixture
def task(project, user):
    """Фикстура для создания задачи"""
    return Task.objects.create(
        title='Test Task',
        description='Test task description',
        project=project,
        creator=user,
        status='todo',
        priority=2
    )

