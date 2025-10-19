#!/usr/bin/env python
"""Создать admin пользователя"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

from django.contrib.auth.models import User

# Создать или обновить admin пользователя
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✅ Пользователь '{username}' обновлен")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Суперпользователь '{username}' создан")

print(f"   Username: {username}")
print(f"   Password: {password}")

