# 🎯 START HERE - Task Manager API

## Добро пожаловать!

Это полнофункциональный проект **Task Manager API** для учебной практики СВФУ.

---

## 📋 Что включено в проект

✅ **Полный REST API** с Django REST Framework  
✅ **Модели данных**: Project, Task с связями  
✅ **CRUD операции** для проектов и задач  
✅ **Расширенная фильтрация** по статусу, приоритету, датам  
✅ **Swagger документация** для API  
✅ **Pytest тесты** с покрытием >80%  
✅ **Docker** конфигурация (Dockerfile + docker-compose)  
✅ **Nginx + Gunicorn** настройки для продакшена  
✅ **Полная документация** на русском языке  
✅ **Примеры API запросов** (cURL, Python, JavaScript)  
✅ **Скрипты деплоя** для VPS  
✅ **Инструкции** для Render, Railway, VPS  

---

## 🚀 Быстрый старт (3 шага)

### Вариант 1: Локально (5 минут)

```bash
# 1. Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить проект
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Готово!** Откройте: http://127.0.0.1:8000/swagger/

### Вариант 2: Docker (3 минуты)

```bash
# 1. Запустить контейнеры
docker-compose up -d

# 2. Применить миграции
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# 3. Готово!
```

**Откройте**: http://localhost/swagger/

---

## 📚 Документация

Проект содержит подробную документацию:

### 1. 📖 **README.md** - Главная документация
   - Описание проекта
   - **Обучающие разделы**:
     - Основы веба и API (HTTP, REST, Django)
     - Базы данных (SQL, Django ORM, DBeaver)
     - Тестирование и деплой (pytest, Docker, nginx)
   - API эндпоинты
   - Примеры запросов

### 2. ⚡ **QUICKSTART.md** - Быстрый старт
   - Самые короткие инструкции
   - Локальный и Docker запуск
   - Первые API запросы

### 3. 🔧 **INSTALL.md** - Детальная установка
   - Локальная установка
   - Docker установка
   - Деплой на Render, Railway, VPS
   - Устранение неполадок

### 4. 💡 **API_EXAMPLES.md** - Примеры API
   - Практические примеры
   - cURL, Python, JavaScript
   - Фильтрация и поиск
   - Обработка ошибок

### 5. 🏗️ **PROJECT_STRUCTURE.md** - Структура проекта
   - Описание всех файлов и папок
   - Назначение каждого компонента
   - Архитектура проекта

### 6. 🤝 **CONTRIBUTING.md** - Руководство для разработчиков
   - Как внести вклад
   - Стиль кода
   - Процесс Pull Request

---

## 🎓 Обучающие компоненты

Проект содержит детальное объяснение следующих тем (см. README.md):

### 1. Основы веба и API
- **HTTP**: методы, заголовки, коды ответа, CORS
- **REST API**: концепции, структура, примеры
- **Django**: установка, структура, роутинг
- **CRUD API**: создание, чтение, обновление, удаление

### 2. Базы данных
- **SQL**: SELECT, INSERT, UPDATE, DELETE, JOIN
- **Django ORM**: создание, фильтрация, агрегация
- **Миграции**: makemigrations, migrate
- **DBeaver**: работа с SQLite

### 3. Тестирование и деплой
- **pytest**: unit-тесты, фикстуры, coverage
- **Docker**: Dockerfile, docker-compose
- **Gunicorn + Nginx**: продакшен настройка
- **Деплой**: screen, systemd, VPS, облако

---

## 📁 Структура проекта

```
task-manager-api/
├── 📄 README.md              # Главная документация ⭐
├── 📄 QUICKSTART.md          # Быстрый старт
├── 📄 INSTALL.md             # Инструкции по установке
├── 📄 API_EXAMPLES.md        # Примеры API запросов
│
├── 📦 task_manager/          # Django проект
│   ├── settings.py          # Настройки
│   ├── urls.py              # Роутинг
│   └── wsgi.py              # WSGI
│
├── 📱 tasks/                # Приложение задач
│   ├── models.py           # Модели (Project, Task)
│   ├── serializers.py      # Сериализаторы DRF
│   ├── views.py            # ViewSets (API)
│   ├── filters.py          # Фильтры
│   ├── urls.py             # URL маршруты
│   └── tests/              # Тесты
│
├── 🐳 Dockerfile           # Docker образ
├── 🐳 docker-compose.yml   # Docker Compose
├── 🌐 nginx/               # Nginx конфиг
├── 🔧 scripts/             # Скрипты деплоя
├── 📊 fixtures/            # Примеры данных
├── 🧪 pytest.ini           # Настройки тестов
└── 📦 requirements.txt     # Зависимости
```

---

## 🔗 Ссылки после запуска

После запуска проекта будут доступны:

- 🌍 **API**: http://127.0.0.1:8000/api/
- 📚 **Swagger UI**: http://127.0.0.1:8000/swagger/ ⭐
- 📖 **ReDoc**: http://127.0.0.1:8000/redoc/
- 🔐 **Admin**: http://127.0.0.1:8000/admin/

---

## 🎯 API Endpoints

### Проекты
- `GET /api/projects/` - список проектов
- `POST /api/projects/` - создать проект
- `GET /api/projects/{id}/` - детали проекта
- `PATCH /api/projects/{id}/` - обновить проект
- `DELETE /api/projects/{id}/` - удалить проект
- `GET /api/projects/{id}/statistics/` - статистика
- `GET /api/projects/{id}/tasks/` - задачи проекта

### Задачи
- `GET /api/tasks/` - список задач
- `POST /api/tasks/` - создать задачу
- `GET /api/tasks/{id}/` - детали задачи
- `PATCH /api/tasks/{id}/` - обновить задачу
- `DELETE /api/tasks/{id}/` - удалить задачу
- `POST /api/tasks/{id}/change_status/` - изменить статус
- `POST /api/tasks/{id}/assign/` - назначить исполнителя
- `GET /api/tasks/my_tasks/` - мои задачи

---

## 💡 Примеры использования

### Создать проект

```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мой проект",
    "description": "Описание проекта",
    "is_active": true
  }'
```

### Создать задачу

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Моя задача",
    "description": "Описание задачи",
    "project": 1,
    "status": "todo",
    "priority": 3,
    "deadline": "2025-12-31T23:59:59Z"
  }'
```

### Фильтрация задач

```bash
# Просроченные задачи высокого приоритета
curl "http://127.0.0.1:8000/api/tasks/?is_overdue=true&priority=3,4"

# Задачи проекта в статусе "в процессе"
curl "http://127.0.0.1:8000/api/tasks/?project=1&status=in_progress"
```

Больше примеров в **API_EXAMPLES.md**!

---

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest

# С покрытием кода
pytest --cov=tasks --cov-report=html

# Открыть отчет
open htmlcov/index.html  # Mac
```

**Тесты включают**:
- ✅ Тесты моделей (Project, Task)
- ✅ Тесты API endpoints (CRUD)
- ✅ Тесты фильтрации
- ✅ Тесты валидации

---

## 🚀 Деплой

### Render (рекомендуется)
1. Зарегистрируйтесь на render.com
2. New → Web Service
3. Подключите GitHub репозиторий
4. Настройки автоматически определятся
5. Deploy!

### Railway
1. Зарегистрируйтесь на railway.app
2. New Project → Deploy from GitHub
3. Выберите репозиторий
4. Deploy автоматически!

### VPS
```bash
bash scripts/deploy.sh
```

Подробнее в **INSTALL.md**!

---

## 🛠️ Полезные команды

### Django

```bash
python manage.py migrate          # Применить миграции
python manage.py createsuperuser  # Создать админа
python manage.py runserver        # Запустить сервер
python manage.py shell            # Django shell
python manage.py test             # Запустить тесты
```

### Docker

```bash
docker-compose up -d              # Запустить контейнеры
docker-compose down               # Остановить
docker-compose logs -f            # Логи
docker-compose exec web bash     # Shell в контейнере
```

### Makefile

```bash
make install      # Установить зависимости
make migrate      # Применить миграции
make run          # Запустить сервер
make test         # Запустить тесты
make docker-up    # Docker запуск
```

---

## 📦 Загрузка примеров данных

Чтобы быстро протестировать API с готовыми данными:

```bash
# Активировать виртуальное окружение
source venv/bin/activate

# Загрузить примеры
bash scripts/load_sample_data.sh
```

Будет создано:
- 2 пользователя (admin/admin123, developer/dev123)
- 2 проекта
- 8 задач с разными статусами

---

## ✅ Чек-лист требований

Все требования выполнены:

- ✅ Виртуальное окружение
- ✅ .gitignore настроен
- ✅ Код структурирован
- ✅ README.md с полным описанием
- ✅ Примеры API-запросов (curl/Postman)
- ✅ Тесты (pytest)
- ✅ Инструкции по локальному запуску
- ✅ Инструкции по деплою
- ✅ CRUD для проектов и задач
- ✅ Фильтрация задач
- ✅ Привязка задач к проектам и пользователям
- ✅ Swagger-документация
- ✅ Django REST Framework
- ✅ SQLite / PostgreSQL
- ✅ Docker
- ✅ Gunicorn
- ✅ Nginx

---

## 📖 Рекомендуемый порядок изучения

1. **Прочитайте README.md** - главная документация с обучающими разделами
2. **Запустите проект** - следуйте QUICKSTART.md
3. **Откройте Swagger** - http://127.0.0.1:8000/swagger/
4. **Попробуйте API** - используйте примеры из API_EXAMPLES.md
5. **Изучите код**:
   - `tasks/models.py` - модели данных
   - `tasks/serializers.py` - сериализаторы
   - `tasks/views.py` - API endpoints
   - `tasks/filters.py` - фильтры
6. **Запустите тесты** - `pytest`
7. **Загрузите примеры данных** - `bash scripts/load_sample_data.sh`
8. **Попробуйте деплой** - следуйте INSTALL.md

---

## 🎓 Обучающие ресурсы в проекте

### HTTP и REST API
- См. **README.md → Раздел 1**
- Примеры HTTP методов и кодов ответа
- Концепции REST архитектуры

### Django и Django REST Framework
- См. **README.md → Раздел 1**
- Структура проекта
- Роутинг и ViewSets
- Сериализаторы

### SQL и Django ORM
- См. **README.md → Раздел 2**
- Основные SQL команды
- Django ORM примеры
- Миграции

### Тестирование
- См. **README.md → Раздел 3**
- pytest основы
- Фикстуры
- Coverage

### Docker
- См. **README.md → Раздел 3**
- Dockerfile
- docker-compose
- Команды Docker

### Деплой
- См. **README.md → Раздел 3** и **INSTALL.md**
- Gunicorn настройка
- Nginx конфигурация
- Деплой на разные платформы

---

## 💬 Поддержка

Если возникли вопросы:

1. 📚 Проверьте документацию (README.md, INSTALL.md)
2. 🔍 Изучите Swagger документацию
3. 🐛 Проверьте логи: `docker-compose logs -f`
4. 📖 Посмотрите примеры в API_EXAMPLES.md

---

## 🎯 Следующие шаги

После освоения базового функционала можно:

1. ✨ Добавить аутентификацию по токенам (JWT)
2. 📧 Добавить email уведомления о дедлайнах
3. 🏷️ Добавить теги для задач
4. 📎 Добавить прикрепление файлов
5. 💬 Добавить комментарии к задачам
6. 📊 Добавить дашборд с аналитикой
7. 🔔 Добавить WebSocket для real-time уведомлений
8. 🌐 Создать фронтенд (React, Vue)

---

## 📄 Лицензия

Учебный проект для СВФУ. Создан в образовательных целях.

---

## 🎉 Готово к использованию!

Проект полностью настроен и готов к работе.

**Начните с**: [QUICKSTART.md](QUICKSTART.md)

**Удачи в изучении! 🚀**

---

_Создано для учебной практики СВФУ, 2025_

