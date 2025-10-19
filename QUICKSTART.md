# Быстрый старт Task Manager API

Это краткое руководство для быстрого запуска проекта.

## Вариант 1: Локальный запуск (5 минут)

### Шаг 1: Клонирование и установка

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt
```

### Шаг 2: Настройка базы данных

```bash
# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser
# Введите: admin / admin@example.com / admin123
```

### Шаг 3: Запуск

```bash
python manage.py runserver
```

✅ Готово! Откройте в браузере:
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/

---

## Вариант 2: Docker (3 минуты)

### Предварительные требования
- Установлен Docker Desktop

### Запуск

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api

# Запустить контейнеры
docker-compose up -d

# Применить миграции
docker-compose exec web python manage.py migrate

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser
```

✅ Готово! Приложение доступно:
- API: http://localhost/api/
- Swagger: http://localhost/swagger/
- Admin: http://localhost/admin/

---

## Первые шаги в API

### 1. Войдите в админку

Откройте http://127.0.0.1:8000/admin/ и войдите с созданными учетными данными.

### 2. Авторизация в API

API поддерживает три способа аутентификации:

#### Способ 1: Bearer Token (рекомендуется) 🔥

```bash
# 1. Получите токен (один раз)
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "gavrilslepcov", "password": "123"}'

# Ответ:
# {"token":"9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}

# 2. Сохраните токен в переменную
export TOKEN="9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"

# 3. Используйте токен в запросах
curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/projects/
```

**Преимущества Bearer Token:**
- ✅ Безопаснее - не передаете пароль в каждом запросе
- ✅ Можно отозвать токен без смены пароля
- ✅ Стандарт для REST API

#### Способ 2: Basic Authentication (для тестирования)

```bash
# Используйте -u username:password в каждом запросе
curl -u admin:admin123 http://127.0.0.1:8000/api/projects/
```

#### Способ 3: Сохранение сессии (для браузера)

```bash
# 1. Войдите через админку http://127.0.0.1:8000/admin/
# 2. Используйте Swagger UI http://127.0.0.1:8000/swagger/
```

**В примерах ниже используется Bearer Token**

### 3. Создайте проект через API

```bash
curl -H "Authorization: Token $TOKEN" \
  -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мой первый проект",
    "description": "Тестовый проект",
    "is_active": true
  }'
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Мой первый проект",
  "description": "Тестовый проект",
  "owner": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "is_active": true,
  "tasks_count": 0,
  "completed_tasks_count": 0,
  "created_at": "2025-10-09T12:00:00Z",
  "updated_at": "2025-10-09T12:00:00Z"
}
```

### 4. Создайте задачу

```bash
curl -H "Authorization: Token $TOKEN" \
  -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Моя первая задача",
    "description": "Тестовая задача",
    "project": 1,
    "status": "todo",
    "priority": 2
  }'
```

**Ответ:**
```json
{
  "id": 1,
  "title": "Моя первая задача",
  "description": "Тестовая задача",
  "project": 1,
  "status": "todo",
  "priority": 2,
  "deadline": null,
  "created_at": "2025-10-09T12:05:00Z"
}
```

### 5. Получите список задач

```bash
# Все задачи
curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/tasks/

# С фильтрацией по статусу
curl -H "Authorization: Token $TOKEN" "http://127.0.0.1:8000/api/tasks/?status=todo"

# С фильтрацией по приоритету
curl -H "Authorization: Token $TOKEN" "http://127.0.0.1:8000/api/tasks/?priority=3&priority=4"
```

### 6. Получите список проектов

```bash
curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/projects/
```

### 7. Обновите задачу

```bash
curl -H "Authorization: Token $TOKEN" \
  -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "priority": 4
  }'
```

### 8. Измените статус задачи

```bash
curl -H "Authorization: Token $TOKEN" \
  -X POST http://127.0.0.1:8000/api/tasks/1/change_status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### 9. Получите статистику проекта

```bash
curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/projects/1/statistics/
```

### 10. Откройте Swagger UI

Перейдите на http://127.0.0.1:8000/swagger/ для интерактивной работы с API.

**В Swagger UI:**
1. Нажмите кнопку "Authorize" вверху справа
2. Войдите через браузер (Session Auth) или используйте Basic Auth
3. Теперь можете выполнять запросы прямо из интерфейса

---

## Запуск тестов

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Запустите тесты
pytest

# С покрытием кода
pytest --cov=tasks --cov-report=html
```

---

## Использование Makefile (опционально)

Если установлен `make`:

```bash
make install      # Установить зависимости
make migrate      # Применить миграции
make run          # Запустить сервер
make test         # Запустить тесты
make docker-up    # Запустить через Docker

# Показать все команды
make help
```

---

## Примеры запросов с авторизацией

### Python

```python
import requests

# 1. Получить токен (один раз)
response = requests.post(
    'http://127.0.0.1:8000/api/auth/token/',
    json={'username': 'admin', 'password': 'admin123'}
)
token = response.json()['token']
print(f"Токен: {token}")

# 2. Настроить заголовки с токеном
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# 3. Получить список проектов
response = requests.get(
    'http://127.0.0.1:8000/api/projects/',
    headers=headers
)
projects = response.json()
print(f"Найдено проектов: {len(projects['results'])}")

# 4. Создать проект
project_data = {
    'name': 'Новый проект',
    'description': 'Описание проекта',
    'is_active': True
}
response = requests.post(
    'http://127.0.0.1:8000/api/projects/',
    json=project_data,
    headers=headers
)
project = response.json()
print(f"Создан проект ID: {project['id']}")

# 5. Создать задачу
task_data = {
    'title': 'Новая задача',
    'description': 'Описание задачи',
    'project': project['id'],
    'status': 'todo',
    'priority': 3
}
response = requests.post(
    'http://127.0.0.1:8000/api/tasks/',
    json=task_data,
    headers=headers
)
task = response.json()
print(f"Создана задача ID: {task['id']}")

# 6. Получить задачи с фильтрацией
response = requests.get(
    'http://127.0.0.1:8000/api/tasks/',
    params={'status': 'todo', 'priority': 3},
    headers=headers
)
tasks = response.json()
print(f"Найдено задач: {tasks['count']}")
```

**Переиспользуемый класс для API:**

```python
import requests

class TaskManagerAPI:
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
    
    def login(self, username, password):
        """Получить токен"""
        response = requests.post(
            f'{self.base_url}/api/auth/token/',
            json={'username': username, 'password': password}
        )
        self.token = response.json()['token']
        self.headers['Authorization'] = f'Token {self.token}'
        return self.token
    
    def get_projects(self, **params):
        """Получить список проектов"""
        response = requests.get(
            f'{self.base_url}/api/projects/',
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def create_project(self, name, description='', is_active=True):
        """Создать проект"""
        response = requests.post(
            f'{self.base_url}/api/projects/',
            json={'name': name, 'description': description, 'is_active': is_active},
            headers=self.headers
        )
        return response.json()
    
    def create_task(self, title, project_id, **kwargs):
        """Создать задачу"""
        data = {'title': title, 'project': project_id, **kwargs}
        response = requests.post(
            f'{self.base_url}/api/tasks/',
            json=data,
            headers=self.headers
        )
        return response.json()

# Использование
api = TaskManagerAPI()
api.login('admin', 'admin123')
projects = api.get_projects()
print(f"Проектов: {projects['count']}")
```

### JavaScript (fetch)

```javascript
// 1. Получить токен
async function getToken(username, password) {
  const response = await fetch('http://127.0.0.1:8000/api/auth/token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  return data.token;
}

// 2. Использовать токен
async function main() {
  const token = await getToken('admin', 'admin123');
  console.log('Токен получен:', token);
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  };

  // Получить список задач
  const tasksResponse = await fetch('http://127.0.0.1:8000/api/tasks/', {
    headers: headers
  });
  const tasks = await tasksResponse.json();
  console.log('Задач найдено:', tasks.count);
  tasks.results.forEach(task => {
    console.log(`- ${task.title} (${task.status})`);
  });

  // Создать проект
  const projectResponse = await fetch('http://127.0.0.1:8000/api/projects/', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({
      name: 'Новый проект',
      description: 'Описание',
      is_active: true
    })
  });
  const project = await projectResponse.json();
  console.log('Создан проект:', project.id);

  // Обновить задачу
  const updateResponse = await fetch('http://127.0.0.1:8000/api/tasks/1/', {
    method: 'PATCH',
    headers: headers,
    body: JSON.stringify({
      status: 'in_progress',
      priority: 4
    })
  });
  const updatedTask = await updateResponse.json();
  console.log('Задача обновлена:', updatedTask.title);
}

main();
```

**Класс-обертка для API:**

```javascript
class TaskManagerAPI {
  constructor(baseURL = 'http://127.0.0.1:8000') {
    this.baseURL = baseURL;
    this.token = null;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseURL}/api/auth/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    this.token = data.token;
    return this.token;
  }

  getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Token ${this.token}`
    };
  }

  async getProjects(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = `${this.baseURL}/api/projects/${queryString ? '?' + queryString : ''}`;
    const response = await fetch(url, { headers: this.getHeaders() });
    return response.json();
  }

  async createProject(name, description = '', isActive = true) {
    const response = await fetch(`${this.baseURL}/api/projects/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ name, description, is_active: isActive })
    });
    return response.json();
  }

  async createTask(title, projectId, data = {}) {
    const response = await fetch(`${this.baseURL}/api/tasks/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ title, project: projectId, ...data })
    });
    return response.json();
  }
}

// Использование
(async () => {
  const api = new TaskManagerAPI();
  await api.login('admin', 'admin123');
  const projects = await api.getProjects();
  console.log('Проектов:', projects.count);
})();
```

### JavaScript (axios)

```javascript
const axios = require('axios');

// 1. Получить токен
async function setupAPI() {
  const tokenResponse = await axios.post(
    'http://127.0.0.1:8000/api/auth/token/',
    { username: 'admin', password: 'admin123' }
  );
  const token = tokenResponse.data.token;

  // 2. Настроить axios с токеном
  const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
      'Authorization': `Token ${token}`
    }
  });

  return api;
}

// Использование
(async () => {
  const api = await setupAPI();

  // Получить проекты
  const projects = await api.get('/projects/');
  console.log('Проектов:', projects.data.count);

  // Создать задачу
  const task = await api.post('/tasks/', {
    title: 'Новая задача',
    description: 'Описание',
    project: 1,
    status: 'todo',
    priority: 2
  });
  console.log('Задача создана:', task.data.id);
})();
```

---

## Структура проекта

```
task-manager-api/
├── task_manager/       # Настройки Django
├── tasks/              # Приложение с API
│   ├── models.py      # Модели Project, Task
│   ├── serializers.py # Сериализаторы DRF
│   ├── views.py       # ViewSets
│   └── tests/         # Тесты
├── requirements.txt   # Зависимости
├── Dockerfile         # Docker образ
└── docker-compose.yml # Docker Compose
```

---

## Полезные ссылки

- 📚 [Полная документация](README.md)
- 🚀 [Инструкция по установке](INSTALL.md)
- 💡 [Примеры API](API_EXAMPLES.md)
- 🔧 [Swagger UI](http://127.0.0.1:8000/swagger/)

---

## Устранение проблем

### Ошибка: "Учетные данные не были предоставлены"

Это означает, что запрос требует авторизации.

**Решение - Bearer Token (рекомендуется):**
```bash
# 1. Получите токен
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Ответ: {"token":"ваш_токен_здесь"}

# 2. Сохраните токен
export TOKEN="ваш_токен_здесь"

# 3. Используйте в запросах
curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/projects/
```

**Или используйте Basic Auth (для тестирования):**
```bash
curl -u admin:admin123 http://127.0.0.1:8000/api/projects/
```

### Ошибка: Port already in use

```bash
# Убить процесс на порту 8000
lsof -ti:8000 | xargs kill -9
```

### Ошибка: ModuleNotFoundError

```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate
pip install -r requirements.txt

# Если не хватает setuptools (Python 3.13)
pip install setuptools
```

### Ошибка: no such table: auth_user

Это означает, что база данных не инициализирована.

**Решение:**
```bash
# Остановите сервер (Ctrl+C)
# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер снова
python manage.py runserver
```

### Ошибка: CSRF token missing

При использовании POST/PUT/PATCH запросов.

**Решение для curl:**
```bash
# Используйте Basic Auth (CSRF не требуется)
curl -u admin:admin123 -X POST ...
```

**Решение для браузера:**
- Войдите через http://127.0.0.1:8000/admin/
- Используйте Swagger UI для запросов

---

## Что дальше?

1. 📖 Изучите [полную документацию](README.md)
2. 🧪 Запустите тесты: `pytest`
3. 🔍 Изучите код в `tasks/models.py`, `tasks/views.py`
4. 💻 Попробуйте создать свои API endpoints
5. 🚀 Деплойте на Render или Railway

---

**Удачи! 🎉**

