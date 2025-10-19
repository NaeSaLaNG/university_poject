# Task Manager API (Менеджер задач)

Полнофункциональный REST API для управления проектами и задачами с использованием Django REST Framework.

## 📋 Описание проекта

Task Manager API - это веб-приложение для управления проектами и задачами. Каждый пользователь может создавать проекты, добавлять задачи, устанавливать приоритеты, статусы и дедлайны.

### Основной функционал

- ✅ CRUD операции для проектов и задач
- 🔍 Расширенная фильтрация задач по статусу, дате, приоритету
- 👥 Привязка задач к проектам и пользователям
- 📊 Статистика по проектам
- 📚 Swagger/ReDoc документация API
- 🔒 Аутентификация пользователей
- 🐳 Docker поддержка
- ✨ Nginx + Gunicorn для продакшена

---

## 🎓 Обучающие компоненты проекта

### 1. Основы веба и API

#### HTTP протокол
- **Методы**: GET, POST, PUT, PATCH, DELETE
  - `GET` - получение данных
  - `POST` - создание новых ресурсов
  - `PUT/PATCH` - обновление существующих ресурсов
  - `DELETE` - удаление ресурсов

- **Коды ответа**:
  - `200 OK` - успешный запрос
  - `201 Created` - ресурс создан
  - `204 No Content` - успешно, но нет данных для возврата
  - `400 Bad Request` - ошибка в запросе
  - `401 Unauthorized` - требуется аутентификация
  - `403 Forbidden` - доступ запрещен
  - `404 Not Found` - ресурс не найден
  - `500 Internal Server Error` - ошибка сервера

- **Заголовки**:
  - `Content-Type: application/json` - формат данных
  - `Authorization: Basic/Bearer` - аутентификация
  - `Accept: application/json` - ожидаемый формат ответа

- **CORS** (Cross-Origin Resource Sharing):
  - Настроен в `settings.py` через `django-cors-headers`
  - Позволяет делать запросы с фронтенда на другом домене

#### REST API концепции

**REST** (Representational State Transfer) - архитектурный стиль для создания веб-сервисов.

Принципы REST:
1. **Клиент-сервер** - разделение ответственности
2. **Stateless** - каждый запрос независим
3. **Кэширование** - ответы могут кэшироваться
4. **Единообразный интерфейс** - стандартные методы и URL
5. **Слоистая система** - архитектура может иметь промежуточные слои

Структура URL в проекте:
```
/api/projects/              - список проектов
/api/projects/{id}/         - конкретный проект
/api/projects/{id}/tasks/   - задачи проекта
/api/tasks/                 - список задач
/api/tasks/{id}/            - конкретная задача
/api/tasks/my_tasks/        - мои задачи
```

#### Django Framework

**Django** - высокоуровневый Python веб-фреймворк.

Структура проекта:
```
task_manager/          # Главный проект
  ├── settings.py     # Настройки проекта
  ├── urls.py         # Главный роутинг
  └── wsgi.py         # WSGI конфигурация

tasks/                # Приложение для задач
  ├── models.py       # Модели данных
  ├── views.py        # Представления (ViewSets)
  ├── serializers.py  # Сериализаторы
  ├── urls.py         # URL маршруты
  └── admin.py        # Админ панель
```

**Роутинг в Django REST Framework**:
- Использует `DefaultRouter` для автоматической генерации URL
- ViewSets предоставляют действия: list, create, retrieve, update, destroy
- Дополнительные действия через декоратор `@action`

#### CRUD API

**CRUD** - Create, Read, Update, Delete - базовые операции с данными.

Примеры в проекте:
- **Create**: `POST /api/projects/` - создание проекта
- **Read**: `GET /api/projects/` - список, `GET /api/projects/{id}/` - детали
- **Update**: `PUT/PATCH /api/projects/{id}/` - обновление
- **Delete**: `DELETE /api/projects/{id}/` - удаление

---

### 2. Базы данных и работа с ними

#### SQL основы

Проект использует SQLite (в разработке) и PostgreSQL (в продакшене).

Основные SQL операции:
```sql
-- SELECT - выборка данных
SELECT * FROM tasks_task WHERE status = 'todo';
SELECT title, priority FROM tasks_task ORDER BY priority DESC;

-- INSERT - вставка данных
INSERT INTO tasks_task (title, description, status, priority, project_id, creator_id)
VALUES ('New Task', 'Description', 'todo', 2, 1, 1);

-- UPDATE - обновление данных
UPDATE tasks_task SET status = 'completed' WHERE id = 1;

-- DELETE - удаление данных
DELETE FROM tasks_task WHERE id = 1;

-- JOIN - объединение таблиц
SELECT t.title, p.name 
FROM tasks_task t 
JOIN tasks_project p ON t.project_id = p.id
WHERE p.owner_id = 1;
```

#### Django ORM

**ORM** (Object-Relational Mapping) - преобразование между объектами Python и таблицами БД.

Примеры из проекта:

```python
# Создание объектов
project = Project.objects.create(
    name='New Project',
    owner=user
)

# Получение объектов
projects = Project.objects.all()
project = Project.objects.get(id=1)
active_projects = Project.objects.filter(is_active=True)

# Обновление
project.name = 'Updated Name'
project.save()

# Или через update
Project.objects.filter(id=1).update(name='Updated Name')

# Удаление
project.delete()

# Связанные объекты (ForeignKey)
tasks = project.tasks.all()  # все задачи проекта
project_of_task = task.project  # проект задачи

# Фильтрация по связанным объектам
tasks = Task.objects.filter(project__owner=user)

# Агрегация
from django.db.models import Count
projects_with_counts = Project.objects.annotate(
    task_count=Count('tasks')
)

# Сложные запросы с Q объектами
from django.db.models import Q
tasks = Task.objects.filter(
    Q(status='todo') | Q(status='in_progress'),
    priority__gte=3
)
```

**Миграции**:
```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Просмотр SQL миграции
python manage.py sqlmigrate tasks 0001
```

#### Работа с SQLite через DBeaver

1. **Установка DBeaver**: https://dbeaver.io/
2. **Подключение к SQLite**:
   - New Database Connection → SQLite
   - Path: путь к `db.sqlite3`
3. **Просмотр таблиц**: tasks_project, tasks_task, auth_user
4. **Выполнение SQL запросов** в SQL Editor
5. **Просмотр связей** через ER-диаграммы

---

### 3. Тестирование и деплой

#### Unit-тестирование с pytest

**Pytest** - фреймворк для тестирования Python приложений.

Структура тестов в проекте:
```
tasks/tests/
  ├── test_models.py       # Тесты моделей
  ├── test_api_projects.py # Тесты API проектов
  └── test_api_tasks.py    # Тесты API задач
```

Примеры тестов:
```python
@pytest.mark.django_db
def test_create_project(authenticated_client, user):
    """Тест создания проекта"""
    url = reverse('tasks:project-list')
    data = {'name': 'Test Project', 'is_active': True}
    response = authenticated_client.post(url, data)
    
    assert response.status_code == 201
    assert Project.objects.count() == 1
```

Запуск тестов:
```bash
# Все тесты
pytest

# С покрытием кода
pytest --cov=tasks --cov-report=html

# Конкретный файл
pytest tasks/tests/test_models.py

# Конкретный тест
pytest tasks/tests/test_models.py::TestProjectModel::test_create_project

# Verbose режим
pytest -v
```

Фикстуры (`conftest.py`):
- Переиспользуемые объекты для тестов
- `@pytest.fixture` декоратор
- Примеры: `user`, `project`, `task`, `authenticated_client`

#### Docker

**Docker** - платформа для контейнеризации приложений.

**Dockerfile** - инструкции для создания образа:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "task_manager.wsgi:application"]
```

**docker-compose.yml** - описание сервисов:
```yaml
services:
  web:      # Django приложение
  db:       # PostgreSQL база данных
  nginx:    # Веб-сервер
```

Команды Docker:
```bash
# Сборка образов
docker-compose build

# Запуск контейнеров
docker-compose up

# Запуск в фоне
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f

# Выполнение команд
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

#### Основы деплоя

**Компоненты продакшен окружения**:

1. **Gunicorn** - WSGI HTTP сервер для Python
   - Запускает Django приложение
   - Настройка: `gunicorn_config.py`
   - Команда: `gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000`

2. **Nginx** - веб-сервер и reverse proxy
   - Обрабатывает статические файлы
   - Проксирует запросы к Gunicorn
   - Балансировка нагрузки
   - SSL терминация

3. **Screen/Systemd** - управление процессами
   - Screen: `screen -S taskmanager`
   - Systemd: автоматический запуск при старте системы

**Деплой на VPS**:
```bash
# Подключение к серверу
ssh user@your-server.com

# Запуск скрипта деплоя
bash scripts/deploy.sh

# Проверка статуса
sudo systemctl status taskmanager
sudo systemctl status nginx

# Просмотр логов
sudo journalctl -u taskmanager -f
```

#### Хостинг платформы

**1. Render** (рекомендуется для начинающих):
- Бесплатный тариф доступен
- Автоматический деплой из GitHub
- Встроенная база данных PostgreSQL
- Шаги:
  1. Зарегистрироваться на render.com
  2. New → Web Service
  3. Подключить GitHub репозиторий
  4. Build Command: `pip install -r requirements.txt`
  5. Start Command: `gunicorn task_manager.wsgi:application`

**2. Railway**:
- Простая настройка
- $5 бесплатных кредитов
- Автоматическое определение Django
- Интеграция с GitHub

**3. VPS (DigitalOcean, AWS, etc.)**:
- Полный контроль
- Требует настройки (см. `scripts/deploy.sh`)
- Установка Nginx, PostgreSQL, настройка systemd

---

## 🚀 Быстрый старт

### Требования

- Python 3.11+
- pip
- virtualenv (опционально)
- Docker и Docker Compose (для контейнеризации)

### Локальная установка

1. **Клонирование репозитория**:
```bash
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api
```

2. **Создание виртуального окружения**:
```bash
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Установка зависимостей**:
```bash
pip install -r requirements.txt
```

4. **Настройка переменных окружения**:
```bash
# Создайте файл .env в корне проекта
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Применение миграций**:
```bash
python manage.py migrate
```

6. **Создание суперпользователя**:
```bash
python manage.py createsuperuser
```

7. **Запуск сервера разработки**:
```bash
python manage.py runserver
```

Приложение доступно по адресу: http://127.0.0.1:8000/

---

## 🐳 Запуск через Docker

1. **Сборка и запуск контейнеров**:
```bash
docker-compose up --build
```

2. **Применение миграций**:
```bash
docker-compose exec web python manage.py migrate
```

3. **Создание суперпользователя**:
```bash
docker-compose exec web python manage.py createsuperuser
```

Приложение доступно:
- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/

---

## 📚 API Документация

### Swagger UI
Интерактивная документация доступна по адресу:
- http://127.0.0.1:8000/swagger/
- http://127.0.0.1:8000/redoc/

### Эндпоинты API

#### Проекты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/projects/` | Список всех проектов |
| POST | `/api/projects/` | Создать новый проект |
| GET | `/api/projects/{id}/` | Получить проект по ID |
| PUT | `/api/projects/{id}/` | Полностью обновить проект |
| PATCH | `/api/projects/{id}/` | Частично обновить проект |
| DELETE | `/api/projects/{id}/` | Удалить проект |
| GET | `/api/projects/{id}/statistics/` | Статистика проекта |
| GET | `/api/projects/{id}/tasks/` | Задачи проекта |

#### Задачи

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/tasks/` | Список всех задач |
| POST | `/api/tasks/` | Создать новую задачу |
| GET | `/api/tasks/{id}/` | Получить задачу по ID |
| PUT | `/api/tasks/{id}/` | Полностью обновить задачу |
| PATCH | `/api/tasks/{id}/` | Частично обновить задачу |
| DELETE | `/api/tasks/{id}/` | Удалить задачу |
| POST | `/api/tasks/{id}/change_status/` | Изменить статус задачи |
| POST | `/api/tasks/{id}/assign/` | Назначить задачу пользователю |
| GET | `/api/tasks/my_tasks/` | Мои задачи |

---

## 💡 Примеры API запросов

### cURL примеры

#### 1. Получить список проектов
```bash
curl -X GET http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json"
```

#### 2. Создать новый проект
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый проект",
    "description": "Описание проекта",
    "is_active": true
  }'
```

#### 3. Получить задачи с фильтрацией по статусу
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?status=todo&priority=3" \
  -H "Content-Type: application/json"
```

#### 4. Создать новую задачу
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новая задача",
    "description": "Описание задачи",
    "project": 1,
    "status": "todo",
    "priority": 3,
    "deadline": "2025-12-31T23:59:59Z"
  }'
```

#### 5. Обновить статус задачи
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/change_status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

#### 6. Назначить задачу пользователю
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/assign/ \
  -H "Content-Type: application/json" \
  -d '{
    "assignee_id": 2
  }'
```

#### 7. Получить статистику проекта
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/statistics/ \
  -H "Content-Type: application/json"
```

#### 8. Фильтрация задач по дате дедлайна
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?deadline_before=2025-12-31" \
  -H "Content-Type: application/json"
```

#### 9. Поиск задач по тексту
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?search=Django" \
  -H "Content-Type: application/json"
```

#### 10. Получить просроченные задачи
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?is_overdue=true" \
  -H "Content-Type: application/json"
```

### Postman Collection

Импортируйте следующую коллекцию в Postman:

```json
{
  "info": {
    "name": "Task Manager API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Projects",
      "item": [
        {
          "name": "Get All Projects",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/projects/",
              "host": ["{{base_url}}"],
              "path": ["api", "projects", ""]
            }
          }
        },
        {
          "name": "Create Project",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"Новый проект\",\n  \"description\": \"Описание\",\n  \"is_active\": true\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/projects/",
              "host": ["{{base_url}}"],
              "path": ["api", "projects", ""]
            }
          }
        }
      ]
    },
    {
      "name": "Tasks",
      "item": [
        {
          "name": "Get All Tasks",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/tasks/",
              "host": ["{{base_url}}"],
              "path": ["api", "tasks", ""]
            }
          }
        },
        {
          "name": "Create Task",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"title\": \"Новая задача\",\n  \"description\": \"Описание\",\n  \"project\": 1,\n  \"status\": \"todo\",\n  \"priority\": 2\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/tasks/",
              "host": ["{{base_url}}"],
              "path": ["api", "tasks", ""]
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000"
    }
  ]
}
```

---

## 🔍 Фильтрация и поиск

### Фильтры для проектов

- `name` - поиск по названию (частичное совпадение)
- `owner` - фильтр по ID владельца
- `is_active` - активные/неактивные проекты
- `created_after` - созданные после даты
- `created_before` - созданные до даты

Пример:
```
GET /api/projects/?is_active=true&name=Django
```

### Фильтры для задач

- `title` - поиск по названию
- `status` - фильтр по статусу (todo, in_progress, review, completed, cancelled)
- `priority` - фильтр по приоритету (1-4)
- `project` - фильтр по ID проекта
- `project_name` - поиск по названию проекта
- `assignee` - фильтр по исполнителю
- `creator` - фильтр по создателю
- `created_after` - созданные после даты
- `created_before` - созданные до даты
- `deadline_after` - дедлайн после даты
- `deadline_before` - дедлайн до даты
- `is_overdue` - просроченные задачи
- `no_assignee` - задачи без исполнителя

Пример:
```
GET /api/tasks/?status=todo&priority=3,4&is_overdue=true
```

### Поиск

Используйте параметр `search` для полнотекстового поиска:
```
GET /api/tasks/?search=Django
```

### Сортировка

Используйте параметр `ordering`:
```
GET /api/tasks/?ordering=-priority,-created_at
```

---

## 🧪 Тестирование

### Запуск всех тестов
```bash
pytest
```

### Запуск с покрытием кода
```bash
pytest --cov=tasks --cov-report=html
```

### Запуск конкретного файла тестов
```bash
pytest tasks/tests/test_models.py
```

### Просмотр отчета о покрытии
```bash
# Генерация отчета
pytest --cov=tasks --cov-report=html

# Открытие в браузере
open htmlcov/index.html  # MacOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## 🚀 Деплой

### Деплой на Render

1. Создайте аккаунт на [render.com](https://render.com)
2. Нажмите "New +" → "Web Service"
3. Подключите GitHub репозиторий
4. Настройки:
   - **Name**: task-manager-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn task_manager.wsgi:application`
5. Добавьте переменные окружения:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.onrender.com`
6. Нажмите "Create Web Service"

### Деплой на Railway

1. Создайте аккаунт на [railway.app](https://railway.app)
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите репозиторий
4. Railway автоматически определит Django проект
5. Добавьте переменные окружения в настройках

### Деплой на VPS

```bash
# На локальной машине
scp scripts/deploy.sh user@your-server.com:~

# На сервере
ssh user@your-server.com
bash deploy.sh
```

---

## 📁 Структура проекта

```
task-manager-api/
├── task_manager/           # Главный проект Django
│   ├── __init__.py
│   ├── settings.py        # Настройки проекта
│   ├── urls.py            # Главный роутинг
│   ├── wsgi.py            # WSGI конфигурация
│   └── asgi.py            # ASGI конфигурация
│
├── tasks/                 # Приложение задач
│   ├── migrations/        # Миграции базы данных
│   ├── tests/             # Тесты
│   │   ├── test_models.py
│   │   ├── test_api_projects.py
│   │   └── test_api_tasks.py
│   ├── __init__.py
│   ├── admin.py           # Админ панель
│   ├── apps.py            # Конфигурация приложения
│   ├── models.py          # Модели данных
│   ├── serializers.py     # Сериализаторы DRF
│   ├── views.py           # ViewSets
│   ├── filters.py         # Фильтры
│   └── urls.py            # URL маршруты
│
├── nginx/                 # Конфигурация Nginx
│   └── nginx.conf
│
├── scripts/               # Скрипты деплоя
│   ├── start.sh
│   └── deploy.sh
│
├── .gitignore            # Игнорируемые файлы
├── .dockerignore         # Игнорируемые файлы для Docker
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose конфигурация
├── requirements.txt      # Python зависимости
├── pytest.ini            # Конфигурация pytest
├── conftest.py           # Фикстуры для тестов
├── gunicorn_config.py    # Конфигурация Gunicorn
├── manage.py             # Django management команды
└── README.md             # Документация
```

---

## 🛠️ Технологии

- **Backend**: Django 4.2, Django REST Framework 3.14
- **База данных**: SQLite (dev), PostgreSQL (prod)
- **Документация**: drf-yasg (Swagger/OpenAPI)
- **Тестирование**: pytest, pytest-django, pytest-cov
- **Сервер**: Gunicorn
- **Веб-сервер**: Nginx
- **Контейнеризация**: Docker, Docker Compose
- **Фильтрация**: django-filter
- **CORS**: django-cors-headers

---

## 📝 Дополнительные команды

### Django management команды

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver

# Сбор статических файлов
python manage.py collectstatic

# Запуск Django shell
python manage.py shell

# Создание дампа базы данных
python manage.py dumpdata > backup.json

# Загрузка дампа
python manage.py loaddata backup.json
```

### Docker команды

```bash
# Сборка образов
docker-compose build

# Запуск контейнеров
docker-compose up

# Запуск в фоновом режиме
docker-compose up -d

# Остановка контейнеров
docker-compose down

# Просмотр логов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f web

# Выполнение команд в контейнере
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web pytest

# Пересборка контейнеров
docker-compose up --build

# Удаление всех контейнеров и volumes
docker-compose down -v
```

---

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 📄 Лицензия

Этот проект создан в образовательных целях для учебной практики СВФУ.

---

## 👤 Автор

**Учебная практика СВФУ**

- Проект: Task Manager API
- Год: 2025

---

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:
1. Проверьте документацию
2. Изучите Swagger документацию: http://127.0.0.1:8000/swagger/
3. Просмотрите логи: `docker-compose logs -f` или `sudo journalctl -u taskmanager -f`

---

## ✅ Чек-лист выполнения требований

- ✅ Виртуальное окружение настроено
- ✅ .gitignore создан
- ✅ Код структурирован
- ✅ README.md с полным описанием
- ✅ Примеры API-запросов (curl/Postman)
- ✅ Тесты написаны (pytest)
- ✅ Инструкции по локальному запуску
- ✅ Инструкции по деплою
- ✅ CRUD для проектов и задач
- ✅ Фильтрация задач по статусу, дате, приоритету
- ✅ Привязка задач к проектам и пользователям
- ✅ Swagger-документация
- ✅ Django REST Framework
- ✅ SQLite (dev) / PostgreSQL (prod)
- ✅ Docker и docker-compose
- ✅ Gunicorn конфигурация
- ✅ Nginx конфигурация

---

**Удачи в изучении веб-разработки! 🚀**

