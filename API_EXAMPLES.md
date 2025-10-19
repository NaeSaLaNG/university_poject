# Примеры использования API

Этот документ содержит практические примеры использования Task Manager API.

## Содержание

1. [Аутентификация](#аутентификация)
2. [Работа с проектами](#работа-с-проектами)
3. [Работа с задачами](#работа-с-задачами)
4. [Фильтрация и поиск](#фильтрация-и-поиск)
5. [Статистика](#статистика)

---

## Аутентификация

API использует Session Authentication для разработки.

### Вход через Django admin

```bash
# Сначала создайте суперпользователя
python manage.py createsuperuser

# Затем войдите через браузер
# http://127.0.0.1:8000/admin/
```

---

## Работа с проектами

### 1. Получить список всех проектов

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json"
```

**Python (requests):**
```python
import requests

response = requests.get('http://127.0.0.1:8000/api/projects/')
projects = response.json()
print(projects)
```

**JavaScript (fetch):**
```javascript
fetch('http://127.0.0.1:8000/api/projects/')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Ответ:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Веб-разработка",
      "description": "Проект по созданию веб-приложения",
      "owner": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "is_active": true,
      "tasks_count": 5,
      "completed_tasks_count": 2,
      "created_at": "2025-10-01T10:00:00Z",
      "updated_at": "2025-10-09T15:30:00Z"
    }
  ]
}
```

### 2. Создать новый проект

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мобильное приложение",
    "description": "Разработка мобильного приложения на Flutter",
    "is_active": true
  }'
```

**Python:**
```python
import requests

data = {
    "name": "Мобильное приложение",
    "description": "Разработка мобильного приложения на Flutter",
    "is_active": True
}

response = requests.post(
    'http://127.0.0.1:8000/api/projects/',
    json=data
)
project = response.json()
print(f"Создан проект: {project['name']}, ID: {project['id']}")
```

### 3. Получить детали проекта

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/ \
  -H "Content-Type: application/json"
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Веб-разработка",
  "description": "Проект по созданию веб-приложения",
  "owner": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "is_active": true,
  "tasks_count": 5,
  "completed_tasks_count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Настроить Django проект",
      "status": "completed",
      "priority": 3
    }
  ],
  "created_at": "2025-10-01T10:00:00Z",
  "updated_at": "2025-10-09T15:30:00Z"
}
```

### 4. Обновить проект

**cURL (PATCH - частичное обновление):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/projects/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Веб-разработка (обновлено)",
    "is_active": false
  }'
```

**Python:**
```python
import requests

data = {"name": "Веб-разработка (обновлено)"}
response = requests.patch(
    'http://127.0.0.1:8000/api/projects/1/',
    json=data
)
```

### 5. Удалить проект

**cURL:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/projects/1/
```

**Python:**
```python
import requests

response = requests.delete('http://127.0.0.1:8000/api/projects/1/')
print(f"Статус: {response.status_code}")  # 204 No Content
```

---

## Работа с задачами

### 1. Получить список всех задач

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json"
```

**Ответ:**
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Настроить Django проект",
      "project": 1,
      "project_name": "Веб-разработка",
      "assignee": {
        "id": 2,
        "username": "developer"
      },
      "creator": {
        "id": 1,
        "username": "admin"
      },
      "status": "completed",
      "status_display": "Завершена",
      "priority": 3,
      "priority_display": "Высокий",
      "deadline": "2025-10-15T23:59:59Z",
      "is_overdue": false,
      "created_at": "2025-10-01T10:00:00Z",
      "updated_at": "2025-10-05T14:20:00Z"
    }
  ]
}
```

### 2. Создать новую задачу

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Разработать API endpoint",
    "description": "Создать REST API для управления пользователями",
    "project": 1,
    "status": "todo",
    "priority": 3,
    "deadline": "2025-10-31T23:59:59Z"
  }'
```

**Python:**
```python
import requests
from datetime import datetime, timedelta

# Создание задачи с дедлайном через неделю
deadline = (datetime.now() + timedelta(days=7)).isoformat()

data = {
    "title": "Разработать API endpoint",
    "description": "Создать REST API для управления пользователями",
    "project": 1,
    "status": "todo",
    "priority": 3,
    "deadline": deadline
}

response = requests.post(
    'http://127.0.0.1:8000/api/tasks/',
    json=data
)
task = response.json()
print(f"Создана задача: {task['title']}, ID: {task['id']}")
```

### 3. Получить детали задачи

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json"
```

### 4. Обновить задачу

**cURL:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "priority": 4
  }'
```

### 5. Изменить статус задачи

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/change_status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

**Python:**
```python
import requests

def change_task_status(task_id, new_status):
    """Изменить статус задачи"""
    url = f'http://127.0.0.1:8000/api/tasks/{task_id}/change_status/'
    data = {"status": new_status}
    response = requests.post(url, json=data)
    return response.json()

# Пример использования
result = change_task_status(1, "in_progress")
print(f"Новый статус: {result['status_display']}")
```

### 6. Назначить задачу пользователю

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/assign/ \
  -H "Content-Type: application/json" \
  -d '{
    "assignee_id": 2
  }'
```

**Python:**
```python
import requests

def assign_task(task_id, user_id):
    """Назначить задачу пользователю"""
    url = f'http://127.0.0.1:8000/api/tasks/{task_id}/assign/'
    data = {"assignee_id": user_id}
    response = requests.post(url, json=data)
    return response.json()

# Назначить задачу пользователю с ID 2
result = assign_task(1, 2)
print(f"Задача назначена: {result['assignee']['username']}")
```

### 7. Получить мои задачи

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/my_tasks/ \
  -H "Content-Type: application/json"
```

---

## Фильтрация и поиск

### 1. Фильтрация задач по статусу

**cURL:**
```bash
# Одно значение
curl -X GET "http://127.0.0.1:8000/api/tasks/?status=todo"

# Несколько значений
curl -X GET "http://127.0.0.1:8000/api/tasks/?status=todo&status=in_progress"
```

**Python:**
```python
import requests

# Получить только задачи "К выполнению" и "В процессе"
params = {
    'status': ['todo', 'in_progress']
}
response = requests.get('http://127.0.0.1:8000/api/tasks/', params=params)
tasks = response.json()['results']

for task in tasks:
    print(f"{task['title']} - {task['status_display']}")
```

### 2. Фильтрация по приоритету

**cURL:**
```bash
# Высокий и критический приоритет
curl -X GET "http://127.0.0.1:8000/api/tasks/?priority=3&priority=4"
```

### 3. Фильтрация по проекту

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?project=1"
```

### 4. Фильтрация по датам

**cURL:**
```bash
# Задачи созданные после определенной даты
curl -X GET "http://127.0.0.1:8000/api/tasks/?created_after=2025-10-01"

# Задачи с дедлайном до определенной даты
curl -X GET "http://127.0.0.1:8000/api/tasks/?deadline_before=2025-10-31"

# Комбинация фильтров
curl -X GET "http://127.0.0.1:8000/api/tasks/?created_after=2025-10-01&deadline_before=2025-10-31"
```

**Python:**
```python
import requests
from datetime import datetime, timedelta

# Задачи с дедлайном в следующие 7 дней
today = datetime.now()
week_later = today + timedelta(days=7)

params = {
    'deadline_after': today.isoformat(),
    'deadline_before': week_later.isoformat(),
    'status': ['todo', 'in_progress']
}

response = requests.get('http://127.0.0.1:8000/api/tasks/', params=params)
upcoming_tasks = response.json()['results']

print("Задачи на ближайшую неделю:")
for task in upcoming_tasks:
    print(f"- {task['title']} (дедлайн: {task['deadline']})")
```

### 5. Просроченные задачи

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?is_overdue=true"
```

**Python:**
```python
import requests

# Получить все просроченные задачи
response = requests.get(
    'http://127.0.0.1:8000/api/tasks/',
    params={'is_overdue': True}
)
overdue_tasks = response.json()['results']

print(f"Найдено просроченных задач: {len(overdue_tasks)}")
for task in overdue_tasks:
    print(f"❗ {task['title']} - дедлайн был {task['deadline']}")
```

### 6. Задачи без исполнителя

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?no_assignee=true"
```

### 7. Поиск по тексту

**cURL:**
```bash
# Поиск в названии и описании
curl -X GET "http://127.0.0.1:8000/api/tasks/?search=Django"
```

**Python:**
```python
import requests

# Поиск задач связанных с Django
response = requests.get(
    'http://127.0.0.1:8000/api/tasks/',
    params={'search': 'Django'}
)
```

### 8. Сортировка

**cURL:**
```bash
# Сортировка по приоритету (по убыванию)
curl -X GET "http://127.0.0.1:8000/api/tasks/?ordering=-priority"

# Сортировка по нескольким полям
curl -X GET "http://127.0.0.1:8000/api/tasks/?ordering=-priority,-created_at"

# По возрастанию (без минуса)
curl -X GET "http://127.0.0.1:8000/api/tasks/?ordering=deadline"
```

### 9. Комплексная фильтрация

**cURL:**
```bash
# Критические задачи в статусе "в процессе" по проекту 1
curl -X GET "http://127.0.0.1:8000/api/tasks/?project=1&status=in_progress&priority=4&ordering=-created_at"
```

**Python - полноценный пример:**
```python
import requests
from datetime import datetime, timedelta

def get_urgent_tasks(project_id=None):
    """
    Получить срочные задачи:
    - Высокий или критический приоритет
    - Не завершены
    - Дедлайн в течение 3 дней или просрочены
    """
    today = datetime.now()
    three_days_later = today + timedelta(days=3)
    
    params = {
        'priority': [3, 4],  # Высокий и критический
        'status': ['todo', 'in_progress', 'review'],
        'deadline_before': three_days_later.isoformat(),
        'ordering': 'deadline'
    }
    
    if project_id:
        params['project'] = project_id
    
    response = requests.get(
        'http://127.0.0.1:8000/api/tasks/',
        params=params
    )
    
    return response.json()['results']

# Использование
urgent_tasks = get_urgent_tasks(project_id=1)
print(f"Найдено срочных задач: {len(urgent_tasks)}")

for task in urgent_tasks:
    status = "⚠️ ПРОСРОЧЕНА" if task['is_overdue'] else "🔔 Скоро дедлайн"
    print(f"{status}: {task['title']} ({task['priority_display']})")
```

---

## Статистика

### 1. Статистика проекта

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/statistics/
```

**Ответ:**
```json
{
  "total_tasks": 10,
  "completed_tasks": 4,
  "in_progress_tasks": 3,
  "todo_tasks": 2,
  "overdue_tasks": 1
}
```

**Python:**
```python
import requests

def get_project_statistics(project_id):
    """Получить статистику проекта"""
    url = f'http://127.0.0.1:8000/api/projects/{project_id}/statistics/'
    response = requests.get(url)
    stats = response.json()
    
    # Вычисляем прогресс
    if stats['total_tasks'] > 0:
        progress = (stats['completed_tasks'] / stats['total_tasks']) * 100
        stats['progress_percent'] = round(progress, 2)
    else:
        stats['progress_percent'] = 0
    
    return stats

# Использование
stats = get_project_statistics(1)
print(f"Прогресс проекта: {stats['progress_percent']}%")
print(f"Завершено: {stats['completed_tasks']}/{stats['total_tasks']}")
print(f"Просрочено: {stats['overdue_tasks']}")
```

### 2. Задачи проекта

**cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/api/projects/1/tasks/?status=in_progress"
```

---

## Пагинация

API использует пагинацию со стандартным размером страницы 10 элементов.

**cURL:**
```bash
# Первая страница
curl -X GET "http://127.0.0.1:8000/api/tasks/"

# Вторая страница
curl -X GET "http://127.0.0.1:8000/api/tasks/?page=2"

# Изменить размер страницы (если поддерживается)
curl -X GET "http://127.0.0.1:8000/api/tasks/?page_size=20"
```

**Python - обработка всех страниц:**
```python
import requests

def get_all_tasks():
    """Получить все задачи со всех страниц"""
    all_tasks = []
    url = 'http://127.0.0.1:8000/api/tasks/'
    
    while url:
        response = requests.get(url)
        data = response.json()
        all_tasks.extend(data['results'])
        url = data['next']  # URL следующей страницы или None
    
    return all_tasks

# Использование
tasks = get_all_tasks()
print(f"Всего задач: {len(tasks)}")
```

---

## Обработка ошибок

**Python - полноценная обработка:**
```python
import requests
from requests.exceptions import RequestException

def create_task_safe(task_data):
    """Безопасное создание задачи с обработкой ошибок"""
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/tasks/',
            json=task_data,
            timeout=10
        )
        response.raise_for_status()  # Вызовет исключение для 4xx и 5xx
        
        return {
            'success': True,
            'data': response.json()
        }
        
    except requests.exceptions.HTTPError as e:
        # Ошибки HTTP (400, 404, 500 и т.д.)
        error_data = e.response.json() if e.response else {}
        return {
            'success': False,
            'error': f"HTTP Error {e.response.status_code}",
            'details': error_data
        }
        
    except requests.exceptions.ConnectionError:
        # Проблемы с подключением
        return {
            'success': False,
            'error': 'Не удалось подключиться к серверу'
        }
        
    except requests.exceptions.Timeout:
        # Превышено время ожидания
        return {
            'success': False,
            'error': 'Превышено время ожидания'
        }
        
    except RequestException as e:
        # Другие ошибки requests
        return {
            'success': False,
            'error': f'Ошибка запроса: {str(e)}'
        }

# Использование
result = create_task_safe({
    "title": "Новая задача",
    "project": 1,
    "status": "todo",
    "priority": 2
})

if result['success']:
    print(f"Задача создана: {result['data']['title']}")
else:
    print(f"Ошибка: {result['error']}")
    if 'details' in result:
        print(f"Детали: {result['details']}")
```

---

## Полезные скрипты

### Скрипт для массового создания задач

```python
import requests

def bulk_create_tasks(project_id, tasks_data):
    """Создать несколько задач для проекта"""
    created_tasks = []
    failed_tasks = []
    
    for task_data in tasks_data:
        task_data['project'] = project_id
        try:
            response = requests.post(
                'http://127.0.0.1:8000/api/tasks/',
                json=task_data
            )
            response.raise_for_status()
            created_tasks.append(response.json())
        except Exception as e:
            failed_tasks.append({'data': task_data, 'error': str(e)})
    
    return {
        'created': created_tasks,
        'failed': failed_tasks
    }

# Пример использования
tasks = [
    {"title": "Задача 1", "status": "todo", "priority": 2},
    {"title": "Задача 2", "status": "todo", "priority": 3},
    {"title": "Задача 3", "status": "todo", "priority": 1},
]

result = bulk_create_tasks(project_id=1, tasks_data=tasks)
print(f"Создано: {len(result['created'])}, Ошибки: {len(result['failed'])}")
```

### Мониторинг просроченных задач

```python
import requests
import time
from datetime import datetime

def monitor_overdue_tasks(interval_seconds=300):
    """Периодически проверять просроченные задачи"""
    while True:
        response = requests.get(
            'http://127.0.0.1:8000/api/tasks/',
            params={'is_overdue': True}
        )
        
        overdue_tasks = response.json()['results']
        
        if overdue_tasks:
            print(f"\n[{datetime.now()}] Найдено просроченных задач: {len(overdue_tasks)}")
            for task in overdue_tasks:
                print(f"  - {task['title']} (проект: {task['project_name']})")
        else:
            print(f"[{datetime.now()}] Просроченных задач нет")
        
        time.sleep(interval_seconds)

# Запуск мониторинга (проверка каждые 5 минут)
# monitor_overdue_tasks(300)
```

---

Это примеры использования Task Manager API. Для более подробной информации см. Swagger документацию: http://127.0.0.1:8000/swagger/

