#!/bin/bash
# Скрипт деплоя на VPS

set -e

echo "=== Task Manager API Deployment ==="

# Переменные
PROJECT_DIR="/var/www/task_manager"
VENV_DIR="$PROJECT_DIR/venv"
REPO_URL="https://github.com/yourusername/task-manager-api.git"

# Обновление системы
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Установка зависимостей
echo "Installing dependencies..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip nginx git

# Клонирование или обновление репозитория
if [ -d "$PROJECT_DIR" ]; then
    echo "Updating project..."
    cd "$PROJECT_DIR"
    git pull origin main
else
    echo "Cloning project..."
    sudo mkdir -p "$PROJECT_DIR"
    sudo chown -R $USER:$USER "$PROJECT_DIR"
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# Создание виртуального окружения
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv "$VENV_DIR"
fi

# Активация виртуального окружения
source "$VENV_DIR/bin/activate"

# Установка Python зависимостей
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Применение миграций
echo "Applying migrations..."
python manage.py migrate

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Настройка Gunicorn systemd service
echo "Setting up Gunicorn service..."
sudo tee /etc/systemd/system/taskmanager.service > /dev/null <<EOF
[Unit]
Description=Task Manager API Gunicorn daemon
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn \\
    --config $PROJECT_DIR/gunicorn_config.py \\
    task_manager.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Настройка Nginx
echo "Setting up Nginx..."
sudo tee /etc/nginx/sites-available/taskmanager > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Активация сайта в Nginx
sudo ln -sf /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Тестирование конфигурации Nginx
echo "Testing Nginx configuration..."
sudo nginx -t

# Перезапуск сервисов
echo "Restarting services..."
sudo systemctl daemon-reload
sudo systemctl enable taskmanager
sudo systemctl restart taskmanager
sudo systemctl restart nginx

echo "=== Deployment completed! ==="
echo "Check status: sudo systemctl status taskmanager"
echo "View logs: sudo journalctl -u taskmanager -f"

