"""
Модели для управления проектами и задачами.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    """
    Модель проекта.
    Проект может содержать множество задач и принадлежит владельцу.
    """
    name = models.CharField(
        max_length=200, 
        verbose_name='Название проекта',
        help_text='Краткое название проекта'
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание',
        help_text='Подробное описание проекта'
    )
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='projects',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата обновления'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активен',
        help_text='Отметьте, если проект активен'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    @property
    def tasks_count(self):
        """Количество задач в проекте"""
        return self.tasks.count()

    @property
    def completed_tasks_count(self):
        """Количество выполненных задач"""
        return self.tasks.filter(status='completed').count()


class Task(models.Model):
    """
    Модель задачи.
    Задача привязана к проекту и может быть назначена пользователю.
    """
    
    # Статусы задач
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В процессе'),
        ('review', 'На проверке'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    # Приоритеты
    PRIORITY_CHOICES = [
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
        (4, 'Критический'),
    ]
    
    title = models.CharField(
        max_length=200, 
        verbose_name='Название задачи'
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name='Проект'
    )
    assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Исполнитель'
    )
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Создатель'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='todo',
        verbose_name='Статус'
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES, 
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name='Приоритет'
    )
    deadline = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Срок выполнения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата обновления'
    )
    completed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Дата завершения'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['project', '-created_at']),
            models.Index(fields=['assignee', 'status']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['deadline']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        """Автоматически устанавливаем дату завершения при изменении статуса"""
        if self.status == 'completed' and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        elif self.status != 'completed':
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Проверка, просрочена ли задача"""
        if self.deadline and self.status not in ['completed', 'cancelled']:
            from django.utils import timezone
            return timezone.now() > self.deadline
        return False

