# Руководство по внесению вклада

Спасибо за интерес к проекту Task Manager API! Мы приветствуем любой вклад.

## Как внести вклад

### 1. Сообщить о проблеме (Issue)

Если вы нашли баг или хотите предложить улучшение:

1. Проверьте, нет ли уже похожей issue
2. Создайте новую issue с детальным описанием:
   - Для багов: шаги воспроизведения, ожидаемое и фактическое поведение
   - Для улучшений: описание предложения и его пользу

### 2. Предложить изменения (Pull Request)

#### Процесс

1. **Fork репозитория**
   ```bash
   # Нажмите кнопку Fork на GitHub
   ```

2. **Клонируйте свой fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/task-manager-api.git
   cd task-manager-api
   ```

3. **Создайте ветку для изменений**
   ```bash
   git checkout -b feature/amazing-feature
   # или
   git checkout -b fix/bug-description
   ```

4. **Настройте окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

5. **Внесите изменения**
   - Следуйте стилю кода проекта
   - Добавьте тесты для новой функциональности
   - Обновите документацию при необходимости

6. **Запустите тесты**
   ```bash
   pytest
   ```

7. **Commit изменений**
   ```bash
   git add .
   git commit -m "feat: добавлена новая функциональность"
   ```

8. **Push в ваш fork**
   ```bash
   git push origin feature/amazing-feature
   ```

9. **Создайте Pull Request**
   - Перейдите на GitHub
   - Нажмите "New Pull Request"
   - Опишите изменения

#### Соглашения о коммитах

Используйте префиксы:
- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование кода
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - рутинные задачи

Примеры:
```bash
git commit -m "feat: добавлена фильтрация задач по тегам"
git commit -m "fix: исправлена ошибка при создании проекта без описания"
git commit -m "docs: обновлена документация API"
```

### 3. Стиль кода

#### Python

Следуйте PEP 8:
```python
# Хорошо
def create_task(title, description, priority=2):
    """Создать новую задачу."""
    task = Task(
        title=title,
        description=description,
        priority=priority
    )
    task.save()
    return task

# Плохо
def createTask(title,description,priority=2):
    task = Task(title=title,description=description,priority=priority)
    task.save()
    return task
```

#### Импорты

Порядок импортов:
1. Стандартная библиотека Python
2. Сторонние библиотеки
3. Django/DRF
4. Локальные импорты

```python
# Стандартная библиотека
import os
from datetime import datetime

# Сторонние библиотеки
import pytest

# Django
from django.db import models
from rest_framework import serializers

# Локальные
from .models import Task
from .utils import helper_function
```

### 4. Тестирование

Все новые функции должны иметь тесты:

```python
@pytest.mark.django_db
def test_create_task(authenticated_client, project):
    """Тест создания задачи"""
    url = reverse('tasks:task-list')
    data = {
        'title': 'Test Task',
        'project': project.id,
        'status': 'todo',
        'priority': 2
    }
    response = authenticated_client.post(url, data)
    
    assert response.status_code == 201
    assert Task.objects.count() == 1
```

Запуск тестов:
```bash
# Все тесты
pytest

# С покрытием
pytest --cov=tasks

# Конкретный файл
pytest tasks/tests/test_models.py

# Verbose
pytest -v
```

### 5. Документация

При добавлении новых API endpoints:

1. **Добавьте docstrings**
   ```python
   @action(detail=True, methods=['post'])
   def custom_action(self, request, pk=None):
       """
       Выполнить пользовательское действие.
       
       Параметры:
       - param1: описание параметра
       
       Возвращает:
       - result: описание результата
       """
       pass
   ```

2. **Обновите README.md** с примерами использования

3. **Добавьте в API_EXAMPLES.md** примеры curl/Python

### 6. Контрольный список перед Pull Request

- [ ] Код соответствует стилю проекта
- [ ] Все тесты проходят (`pytest`)
- [ ] Добавлены тесты для новой функциональности
- [ ] Обновлена документация
- [ ] Commit сообщения понятны и следуют соглашениям
- [ ] Нет конфликтов с основной веткой

### 7. Процесс ревью

1. Один из мейнтейнеров рассмотрит ваш PR
2. Могут быть запрошены изменения
3. После одобрения PR будет смержен

## Вопросы?

Если у вас есть вопросы, создайте issue с меткой "question".

## Кодекс поведения

- Будьте уважительны к другим участникам
- Конструктивная критика приветствуется
- Помогайте новичкам

---

Спасибо за ваш вклад в проект! 🚀

