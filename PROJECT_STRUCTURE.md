# Структура проекта Task Manager API

Полное описание файловой структуры проекта с объяснением назначения каждого файла.

## 📁 Корневая директория

```
task-manager-api/
├── task_manager/          # Главный пакет Django проекта
├── tasks/                 # Django приложение для управления задачами
├── nginx/                 # Конфигурация Nginx
├── scripts/               # Вспомогательные скрипты
├── fixtures/              # Фикстуры с примерами данных
├── requirements.txt       # Python зависимости
├── manage.py             # Django management скрипт
├── pytest.ini            # Конфигурация pytest
├── conftest.py           # Фикстуры для тестов
├── gunicorn_config.py    # Конфигурация Gunicorn
├── Dockerfile            # Инструкции для Docker образа
├── docker-compose.yml    # Конфигурация Docker Compose
├── .gitignore           # Игнорируемые Git файлы
├── .dockerignore        # Игнорируемые Docker файлы
├── Makefile             # Команды для автоматизации
└── README.md            # Основная документация
```

---

## 📦 task_manager/ - Главный проект

Основной пакет Django проекта с настройками и конфигурацией.

```
task_manager/
├── __init__.py          # Python пакет
├── settings.py          # Настройки Django
├── urls.py              # Главный URL роутинг
├── wsgi.py             # WSGI entry point
└── asgi.py             # ASGI entry point (для async)
```

### settings.py
**Назначение**: Центральный конфигурационный файл Django.

**Ключевые настройки**:
- `INSTALLED_APPS` - установленные приложения
- `DATABASES` - конфигурация БД (SQLite по умолчанию)
- `REST_FRAMEWORK` - настройки DRF (пагинация, фильтры)
- `CORS_ALLOWED_ORIGINS` - разрешенные источники для CORS
- `SWAGGER_SETTINGS` - настройки документации

### urls.py
**Назначение**: Главный маршрутизатор URL.

**Маршруты**:
- `/admin/` - админ панель Django
- `/api/` - API endpoints (делегирует в tasks.urls)
- `/swagger/` - Swagger UI документация
- `/redoc/` - ReDoc документация

### wsgi.py
**Назначение**: WSGI интерфейс для развертывания.

**Использование**: Gunicorn использует этот файл для запуска приложения.

---

## 📱 tasks/ - Приложение управления задачами

Основное Django приложение с бизнес-логикой.

```
tasks/
├── migrations/          # Миграции базы данных
├── tests/              # Тесты приложения
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_api_projects.py
│   └── test_api_tasks.py
├── __init__.py
├── admin.py           # Регистрация моделей в админке
├── apps.py            # Конфигурация приложения
├── models.py          # Модели данных (Project, Task)
├── serializers.py     # Сериализаторы DRF
├── views.py           # ViewSets для API
├── filters.py         # Фильтры для запросов
└── urls.py            # URL маршруты приложения
```

### models.py
**Назначение**: Определение моделей данных.

**Модели**:
1. **Project** - Проект с задачами
   - Поля: name, description, owner, is_active
   - Связи: One-to-Many с Task
   - Методы: tasks_count, completed_tasks_count

2. **Task** - Задача
   - Поля: title, description, status, priority, deadline
   - Связи: ForeignKey к Project, User (creator, assignee)
   - Методы: is_overdue, auto-set completed_at

**Индексы**: Оптимизированы для частых запросов.

### serializers.py
**Назначение**: Преобразование моделей в JSON и обратно.

**Сериализаторы**:
- `ProjectListSerializer` - краткая информация о проектах
- `ProjectDetailSerializer` - детальная информация с задачами
- `TaskListSerializer` - список задач
- `TaskDetailSerializer` - детали задачи
- `TaskCreateUpdateSerializer` - создание/обновление
- `UserSerializer` - информация о пользователе

**Валидация**: Проверка дедлайнов, прав доступа.

### views.py
**Назначение**: API endpoints через ViewSets.

**ViewSets**:
1. **ProjectViewSet**
   - CRUD операции для проектов
   - Действия: statistics, tasks
   - Фильтры: по владельцу, активности, датам

2. **TaskViewSet**
   - CRUD операции для задач
   - Действия: change_status, assign, my_tasks
   - Фильтры: по статусу, приоритету, датам, проекту

**Permissions**: IsAuthenticatedOrReadOnly по умолчанию.

### filters.py
**Назначение**: Классы фильтров для django-filter.

**Фильтры**:
- `ProjectFilter` - фильтрация проектов
- `TaskFilter` - расширенная фильтрация задач
  - По статусу, приоритету, датам
  - Просроченные задачи
  - Без исполнителя

### admin.py
**Назначение**: Настройка админ панели Django.

**Возможности**:
- Списки с фильтрами
- Поиск по полям
- Readonly поля
- Группировка полей (fieldsets)
- Custom методы отображения

### tests/
**Назначение**: Тесты приложения.

**Файлы тестов**:
- `test_models.py` - тесты моделей
- `test_api_projects.py` - тесты API проектов
- `test_api_tasks.py` - тесты API задач

**Покрытие**: >80% кода.

---

## 🌐 nginx/ - Конфигурация Nginx

```
nginx/
└── nginx.conf          # Конфигурация веб-сервера
```

### nginx.conf
**Назначение**: Конфигурация Nginx для продакшена.

**Функции**:
- Проксирование к Gunicorn
- Раздача статических файлов
- Сжатие gzip
- Кеширование
- Настройки безопасности

---

## 🔧 scripts/ - Вспомогательные скрипты

```
scripts/
├── start.sh            # Скрипт запуска в Docker
├── deploy.sh          # Скрипт деплоя на VPS
└── load_sample_data.sh # Загрузка примеров данных
```

### start.sh
**Назначение**: Запуск приложения в Docker контейнере.

**Выполняет**:
- Ожидание БД
- Миграции
- Сбор статики
- Создание суперпользователя
- Запуск Gunicorn

### deploy.sh
**Назначение**: Автоматизация деплоя на VPS.

**Выполняет**:
- Обновление системы
- Установка зависимостей
- Клонирование/обновление кода
- Настройка systemd
- Настройка Nginx

### load_sample_data.sh
**Назначение**: Загрузка примеров данных.

**Создает**:
- 2 тестовых пользователя
- 2 проекта
- 8 задач с разными статусами

---

## 📊 fixtures/ - Примеры данных

```
fixtures/
└── sample_data.json    # JSON с тестовыми данными
```

### sample_data.json
**Назначение**: Фикстуры для демонстрации.

**Содержит**:
- Пользователей (admin, developer)
- Проекты
- Задачи с разными статусами и приоритетами

**Загрузка**: `python manage.py loaddata fixtures/sample_data.json`

---

## 📄 Конфигурационные файлы

### requirements.txt
**Назначение**: Python зависимости проекта.

**Основные пакеты**:
- Django 4.2
- djangorestframework 3.14
- django-filter (фильтрация)
- drf-yasg (Swagger)
- gunicorn (WSGI сервер)
- pytest (тестирование)

### Dockerfile
**Назначение**: Инструкции для создания Docker образа.

**Этапы**:
1. Базовый образ Python 3.11
2. Установка системных зависимостей
3. Копирование и установка Python пакетов
4. Копирование кода
5. Сбор статики
6. Создание непривилегированного пользователя
7. Команда запуска (Gunicorn)

### docker-compose.yml
**Назначение**: Описание сервисов для Docker Compose.

**Сервисы**:
- `web` - Django приложение (Gunicorn)
- `db` - PostgreSQL база данных
- `nginx` - Веб-сервер

**Volumes**:
- `postgres_data` - данные PostgreSQL
- `static_volume` - статические файлы

### pytest.ini
**Назначение**: Конфигурация pytest.

**Настройки**:
- Django settings модуль
- Паттерны файлов тестов
- Опции запуска (verbose, coverage)
- Маркеры тестов

### conftest.py
**Назначение**: Общие фикстуры для pytest.

**Фикстуры**:
- `api_client` - тестовый клиент API
- `user` - тестовый пользователь
- `authenticated_client` - аутентифицированный клиент
- `project` - тестовый проект
- `task` - тестовая задача

### gunicorn_config.py
**Назначение**: Конфигурация Gunicorn WSGI сервера.

**Настройки**:
- Bind адрес и порт
- Количество workers
- Таймауты
- Логирование
- Хуки жизненного цикла

### Makefile
**Назначение**: Автоматизация команд через make.

**Команды**:
- `make install` - установка зависимостей
- `make migrate` - применение миграций
- `make run` - запуск сервера
- `make test` - запуск тестов
- `make docker-up` - запуск Docker

### .gitignore
**Назначение**: Игнорирование файлов в Git.

**Игнорирует**:
- Python кеш (\__pycache__, *.pyc)
- Виртуальное окружение (venv/)
- База данных (db.sqlite3)
- Переменные окружения (.env)
- IDE файлы (.vscode/, .idea/)
- Тестовое покрытие (.coverage, htmlcov/)

### .dockerignore
**Назначение**: Игнорирование файлов при сборке Docker.

**Исключает**:
- Виртуальное окружение
- Git файлы
- Документацию
- Тестовые данные

---

## 📚 Документация

```
README.md              # Главная документация
INSTALL.md            # Инструкции по установке
API_EXAMPLES.md       # Примеры использования API
QUICKSTART.md         # Быстрый старт
CONTRIBUTING.md       # Руководство для контрибьюторов
PROJECT_STRUCTURE.md  # Этот файл
```

### README.md
**Содержит**:
- Описание проекта
- Обучающие компоненты (HTTP, REST, Django, SQL, Docker)
- Быстрый старт
- API документация
- Примеры запросов
- Инструкции по деплою

### INSTALL.md
**Содержит**:
- Подробные инструкции по установке
- Локальная установка
- Docker установка
- Деплой на различные платформы (Render, Railway, VPS)
- Устранение неполадок

### API_EXAMPLES.md
**Содержит**:
- Практические примеры использования API
- cURL команды
- Python код
- JavaScript примеры
- Обработка ошибок
- Полезные скрипты

### QUICKSTART.md
**Содержит**:
- Краткое руководство для быстрого старта
- Минимальные шаги для запуска
- Первые запросы к API
- Ссылки на детальную документацию

### CONTRIBUTING.md
**Содержит**:
- Руководство по внесению вклада
- Процесс создания Pull Request
- Соглашения о коде и коммитах
- Требования к тестам
- Кодекс поведения

---

## 🗄️ База данных

### SQLite (разработка)
**Файл**: `db.sqlite3` (создается автоматически)

**Таблицы**:
- `tasks_project` - проекты
- `tasks_task` - задачи
- `auth_user` - пользователи
- `django_session` - сессии
- и другие служебные таблицы Django

### PostgreSQL (продакшен)
**Использование**: В Docker Compose и продакшене

**Подключение**: Через DATABASE_URL в переменных окружения

---

## 🔐 Безопасность

### Переменные окружения
**Файл**: `.env` (не в Git!)

**Переменные**:
- `SECRET_KEY` - секретный ключ Django
- `DEBUG` - режим отладки
- `ALLOWED_HOSTS` - разрешенные хосты
- `DATABASE_URL` - URL базы данных

### Пароли
- Хешируются через Django (PBKDF2)
- Не хранятся в открытом виде
- Требования к сложности в валидаторах

---

## 📈 Масштабирование

### Горизонтальное
- Несколько Gunicorn workers
- Балансировка через Nginx
- Отдельные контейнеры для сервисов

### Вертикальное
- Увеличение workers в gunicorn_config.py
- Оптимизация запросов БД
- Кеширование (Redis можно добавить)

---

## 🧪 Тестирование

### Типы тестов
- **Unit тесты** - модели, функции
- **Integration тесты** - API endpoints
- **Coverage** - покрытие кода тестами

### Запуск
```bash
pytest                    # Все тесты
pytest --cov=tasks       # С покрытием
pytest -v                # Verbose
pytest -k test_create    # Конкретные тесты
```

---

## 🚀 Деплой

### Окружения

1. **Development** (разработка)
   - SQLite
   - DEBUG=True
   - Django runserver

2. **Staging** (тестирование)
   - PostgreSQL
   - DEBUG=True
   - Gunicorn + Nginx

3. **Production** (продакшен)
   - PostgreSQL
   - DEBUG=False
   - Gunicorn + Nginx
   - SSL сертификат
   - Мониторинг

---

Это полное описание структуры проекта Task Manager API. Для более подробной информации о конкретных компонентах см. комментарии в исходном коде.

