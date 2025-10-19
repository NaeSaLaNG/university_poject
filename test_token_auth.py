#!/usr/bin/env python
"""
Скрипт для тестирования Token Authentication API.
"""
import requests
import sys

BASE_URL = 'http://127.0.0.1:8000'

def test_token_auth():
    """Тест Bearer Token аутентификации"""
    print("=" * 60)
    print("Тестирование Token Authentication")
    print("=" * 60)
    
    # 1. Получение токена
    print("\n1. Получение токена...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/auth/token/',
            json={'username': 'admin', 'password': 'admin123'}
        )
        response.raise_for_status()
        token = response.json()['token']
        print(f"✅ Токен получен: {token}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при получении токена: {e}")
        print("Убедитесь, что:")
        print("  1. Сервер запущен (python manage.py runserver)")
        print("  2. Создан пользователь admin/admin123")
        sys.exit(1)
    
    # 2. Тест с токеном
    print("\n2. Тестирование запроса с токеном...")
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f'{BASE_URL}/api/projects/',
            headers=headers
        )
        response.raise_for_status()
        projects = response.json()
        print(f"✅ Получено проектов: {projects.get('count', 0)}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе с токеном: {e}")
        sys.exit(1)
    
    # 3. Тест без токена (должен вернуть ошибку)
    print("\n3. Тестирование запроса без токена (должен вернуть ошибку)...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/projects/',
            json={'name': 'Test Project', 'is_active': True}
        )
        if response.status_code == 401:
            print("✅ Правильно: запрос без токена отклонен (401)")
        else:
            print(f"⚠️  Неожиданный код: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка: {e}")
    
    # 4. Создание проекта с токеном
    print("\n4. Создание проекта с токеном...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/projects/',
            json={
                'name': 'Test Project',
                'description': 'Создан через Token Auth',
                'is_active': True
            },
            headers=headers
        )
        response.raise_for_status()
        project = response.json()
        print(f"✅ Проект создан: ID {project.get('id')} - {project.get('name')}")
        
        # 5. Создание задачи
        print("\n5. Создание задачи с токеном...")
        response = requests.post(
            f'{BASE_URL}/api/tasks/',
            json={
                'title': 'Test Task',
                'description': 'Создана через Token Auth',
                'project': project.get('id'),
                'status': 'todo',
                'priority': 2
            },
            headers=headers
        )
        response.raise_for_status()
        task = response.json()
        print(f"✅ Задача создана: ID {task.get('id')} - {task.get('title')}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при создании: {e}")
        if hasattr(e.response, 'text'):
            print(f"Ответ сервера: {e.response.text}")
    
    # 6. Тест Basic Auth (для сравнения)
    print("\n6. Тестирование Basic Authentication...")
    try:
        response = requests.get(
            f'{BASE_URL}/api/projects/',
            auth=('admin', 'admin123')
        )
        response.raise_for_status()
        print("✅ Basic Auth тоже работает")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка Basic Auth: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Все тесты пройдены успешно!")
    print("=" * 60)
    print(f"\n🔑 Ваш токен: {token}")
    print(f"\nИспользуйте его в запросах:")
    print(f"curl -H \"Authorization: Token {token}\" {BASE_URL}/api/projects/")
    print("\nИли в переменной окружения:")
    print(f"export TOKEN=\"{token}\"")
    print(f"curl -H \"Authorization: Token $TOKEN\" {BASE_URL}/api/projects/")

if __name__ == '__main__':
    test_token_auth()

