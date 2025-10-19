# Инструкция по установке Task Manager API

## Локальная установка (разработка)

### 1. Подготовка окружения

#### Установка Python
```bash
# Проверьте версию Python (должна быть 3.11+)
python --version

# Если нужно установить Python 3.11
# macOS (через Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Windows - скачайте с https://www.python.org/downloads/
```

### 2. Клонирование проекта

```bash
git clone ssh-url
cd task-manager-api
```

### 3. Создание виртуального окружения

```bash
# Linux/MacOS
python3.11 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Установка зависимостей

```bash
# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Django настройки
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# База данных (по умолчанию SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 6. Инициализация базы данных

```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
# Введите: username, email, password
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу:
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/

---

## Установка через Docker

### 1. Установка Docker

#### macOS
```bash
# Скачайте Docker Desktop с https://www.docker.com/products/docker-desktop
```

#### Ubuntu/Debian
```bash
# Обновление пакетов
sudo apt update

# Установка Docker
sudo apt install docker.io docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```

#### Windows
```bash
# Скачайте Docker Desktop с https://www.docker.com/products/docker-desktop
```

### 2. Запуск проекта

```bash
# Сборка и запуск контейнеров
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d
```

### 3. Инициализация базы данных

```bash
# Применение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser
```

### 4. Доступ к приложению

- API: http://localhost/api/
- Swagger: http://localhost/swagger/
- Admin: http://localhost/admin/

---

## Деплой на Render

### 1. Подготовка

1. Зарегистрируйтесь на [render.com](https://render.com)
2. Создайте GitHub репозиторий и загрузите код
3. Подключите GitHub аккаунт к Render

### 2. Создание Web Service

1. В Render Dashboard нажмите "New +" → "Web Service"
2. Выберите ваш репозиторий
3. Настройки:
   - **Name**: task-manager-api
   - **Region**: выберите ближайший
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn task_manager.wsgi:application`

### 3. Переменные окружения

Добавьте в Environment:
```
SECRET_KEY=ваш-безопасный-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=postgresql://... (автоматически если создали БД)
```

### 4. База данных

1. Нажмите "New +" → "PostgreSQL"
2. Создайте базу данных
3. Скопируйте Internal Database URL
4. Добавьте в переменные окружения Web Service

### 5. Деплой

1. Нажмите "Create Web Service"
2. Дождитесь завершения деплоя
3. Ваше приложение доступно по URL: `https://your-app.onrender.com`

---

## Деплой на Railway

### 1. Подготовка

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Создайте GitHub репозиторий

### 2. Деплой

1. В Railway нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий
4. Railway автоматически определит Django и настроит

### 3. База данных

1. В проекте нажмите "New" → "Database" → "PostgreSQL"
2. Railway автоматически добавит DATABASE_URL

### 4. Переменные окружения

Добавьте в Variables:
```
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

### 5. Настройка домена

1. Перейдите в Settings → Domains
2. Сгенерируйте домен или добавьте кастомный

---

## Деплой на VPS (DigitalOcean, AWS, etc.)

### 1. Подготовка сервера

```bash
# Подключение к серверу
ssh root@your-server-ip

# Обновление системы
apt update && apt upgrade -y

# Установка зависимостей
apt install -y python3.11 python3.11-venv python3-pip \
    nginx git postgresql postgresql-contrib
```

### 2. Создание пользователя

```bash
# Создание пользователя для приложения
adduser taskmanager
usermod -aG sudo taskmanager
su - taskmanager
```

### 3. Клонирование проекта

```bash
cd /var/www
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api
```

### 4. Виртуальное окружение

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Настройка PostgreSQL

```bash
# Переключение на пользователя postgres
sudo -u postgres psql

# В PostgreSQL консоли
CREATE DATABASE taskmanager;
CREATE USER taskmanager WITH PASSWORD 'secure_password';
ALTER ROLE taskmanager SET client_encoding TO 'utf8';
ALTER ROLE taskmanager SET default_transaction_isolation TO 'read committed';
ALTER ROLE taskmanager SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskmanager;
\q
```

### 6. Переменные окружения

```bash
# Создайте .env файл
cat > .env << EOF
SECRET_KEY=ваш-безопасный-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://taskmanager:secure_password@localhost/taskmanager
EOF
```

### 7. Миграции и статика

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 8. Настройка Gunicorn и Systemd

```bash
# Создание systemd service
sudo nano /etc/systemd/system/taskmanager.service
```

Содержимое файла:
```ini
[Unit]
Description=Task Manager API Gunicorn daemon
After=network.target

[Service]
User=taskmanager
Group=www-data
WorkingDirectory=/var/www/task-manager-api
Environment="PATH=/var/www/task-manager-api/venv/bin"
ExecStart=/var/www/task-manager-api/venv/bin/gunicorn \
    --config /var/www/task-manager-api/gunicorn_config.py \
    task_manager.wsgi:application

[Install]
WantedBy=multi-user.target
```

Запуск сервиса:
```bash
sudo systemctl start taskmanager
sudo systemctl enable taskmanager
sudo systemctl status taskmanager
```

### 9. Настройка Nginx

```bash
sudo nano /etc/nginx/sites-available/taskmanager
```

Содержимое:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location /static/ {
        alias /var/www/task-manager-api/staticfiles/;
    }

    location /media/ {
        alias /var/www/task-manager-api/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активация:
```bash
sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. SSL сертификат (Let's Encrypt)

```bash
# Установка certbot
sudo apt install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Автоматическое обновление
sudo systemctl status certbot.timer
```

---

## Устранение неполадок

### Проблема: ModuleNotFoundError

**Решение**: Убедитесь, что виртуальное окружение активировано и зависимости установлены
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Проблема: Database connection error

**Решение**: Проверьте настройки базы данных в `.env` файле

### Проблема: Port already in use

**Решение**: Остановите процесс, использующий порт
```bash
# Найти процесс
lsof -i :8000

# Убить процесс
kill -9 <PID>
```

### Проблема: Static files not found

**Решение**: Соберите статические файлы
```bash
python manage.py collectstatic --noinput
```

### Проблема: Migration conflicts

**Решение**: Сбросьте миграции
```bash
# Удалите db.sqlite3 (только для разработки!)
rm db.sqlite3

# Удалите файлы миграций (кроме __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Создайте миграции заново
python manage.py makemigrations
python manage.py migrate
```

---

## Полезные команды

```bash
# Просмотр логов (systemd)
sudo journalctl -u taskmanager -f

# Перезапуск сервисов
sudo systemctl restart taskmanager
sudo systemctl restart nginx

# Обновление кода из git
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart taskmanager

# Бэкап базы данных
python manage.py dumpdata > backup.json

# Восстановление из бэкапа
python manage.py loaddata backup.json
```

---

## Проверка установки

После установки проверьте:

1. ✅ API доступен: `curl http://localhost:8000/api/`
2. ✅ Swagger работает: http://localhost:8000/swagger/
3. ✅ Admin панель: http://localhost:8000/admin/
4. ✅ Тесты проходят: `pytest`
5. ✅ Создание проекта: `curl -X POST ...`

Если все работает - установка завершена успешно! 🎉

