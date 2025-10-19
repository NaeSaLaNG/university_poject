#!/bin/bash
# Скрипт для загрузки примеров данных

set -e

echo "=== Загрузка примеров данных ==="

# Проверка, что виртуальное окружение активировано
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Виртуальное окружение не активировано!"
    echo "Запустите: source venv/bin/activate"
    exit 1
fi

# Применение миграций
echo "1. Применение миграций..."
python manage.py migrate

# Загрузка данных
echo "2. Загрузка примеров данных..."
python manage.py loaddata fixtures/sample_data.json

# Установка паролей для пользователей
echo "3. Установка паролей для пользователей..."
python manage.py shell << END
from django.contrib.auth.models import User

# Установить пароль для admin
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.save()

# Установить пароль для developer
developer = User.objects.get(username='developer')
developer.set_password('dev123')
developer.save()

print("Пароли установлены:")
print("  admin:admin123")
print("  developer:dev123")
END

echo ""
echo "✅ Примеры данных успешно загружены!"
echo ""
echo "Тестовые пользователи:"
echo "  - admin / admin123 (суперпользователь)"
echo "  - developer / dev123"
echo ""
echo "Создано проектов: 2"
echo "Создано задач: 8"
echo ""
echo "Запустите сервер: python manage.py runserver"
echo "Откройте: http://127.0.0.1:8000/swagger/"

