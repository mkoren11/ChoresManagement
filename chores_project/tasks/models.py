# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Task(models.Model):
    """
    Основна модель завдання
    """
    
    # Статуси завдань
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('in_progress', 'В роботі'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
        ('on_hold', 'Призупинено'),
    ]
    
    # Пріоритети
    PRIORITY_CHOICES = [
        ('low', 'Низький'),
        ('medium', 'Середній'),
        ('high', 'Високий'),
        ('urgent', 'Терміново'),
    ]
    
    # Основні поля
    title = models.CharField(
       max_length=200,
       verbose_name='Назва завдання',
        help_text='Коротка назва завдання' 
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Опис',
        help_text='Детальний опис завдання'
    )
    
    status = models.CharField(
       max_length=20,
       choices=STATUS_CHOICES,
       default='pending',
       verbose_name='Статус',
       db_index=True
    )
    
    priority = models.CharField(
       max_length=10,
       choices=PRIORITY_CHOICES,
       default='medium',
       verbose_name='Приорітет',
       db_index=True
    )
    
    # Дати та час
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Створено'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Оновлено'
    )
    
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Термін виконання',
        help_text='Дата і час до якого має бути виконано завдання'
    )
    
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Початок роботи'
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Завершено'
    )
    
    # Прогрес виконання (0-100%)
    progress = models.PositiveSmallIntegerField(
       default=0,
       validators=[MinValueValidator(0), MaxValueValidator(100)],
       verbose_name='Прогрес (%)',
       help_text='Відсоток виконання завдання'
    )
    
    # Оцінка часу на виконання (в хвилинах)
    estimated_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Оцінка часу (години)',
        help_text='Приблизний час на виконання завдання'
    )
    
    # Фактично витрачений час (в хвилинах)
    actual_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Фактичний час (години)',
        help_text='Реально витрачений час на завдання'
    )
    
    # Нотатки та коментарі
    notes = models.TextField(
        blank=True,
        verbose_name='Нотатки',
        help_text='Додаткові нотатки по завданню'
    )
    
    # Теги (як простий текст, поки без зв'язків)
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Теги',
        help_text='Теги через кому для категоризації завдань'
    )
    
    # Активність завдання
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активне',
        help_text='Чи є завдання активним'
    )
    
    # Архівне завдання
    is_archived = models.BooleanField(
        default=False,
        verbose_name='Архівне',
        help_text='Чи знаходиться завдання в архіві',
        db_index=True
    )
    
    # Заглушки для майбутніх зв'язків
    
    # TODO: Зв'язок з категоріями завдань
    # category = models.ForeignKey(
    #     'TaskCategory',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='tasks'
    # )
    
    # TODO: Зв'язок з користувачем (виконавець)
    # assigned_to = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='assigned_tasks'
    # )
    
    # TODO: Зв'язок з автором завдання
    # created_by = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='created_tasks'
    # )
    
    # TODO: Зв'язок з шаблоном завдання
    # template = models.ForeignKey(
    #     'TaskTemplate',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='tasks'
    # )
    
    # TODO: Зв'язок з повторюваними завданнями
    # recurring_task = models.ForeignKey(
    #     'RecurringTask',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='tasks'
    # )
    
    # TODO: Зв'язок з батьківським завданням (підзавдання)
    # parent_task = models.ForeignKey(
    #     'self',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='subtasks'
    # )
    
    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'
        ordering = ['-created_at', '-priority']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['due_date']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active', 'is_archived']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        if self.status == 'in_progress' and not self.started_at:
            self.started_at = timezone.now()

        if self.status == 'completed':
            if not self.completed_at:
                self.completed_at = timezone.now()
            if self.progress < 100:
                self.progress = 100

        if self.status != 'completed' and self.completed_at:
            self.completed_at = None

        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """
        Перевіряє, чи прострочене завдання
        """
        if not self.due_date or self.status == 'completed':
            return False
        return timezone.now() > self.due_date
    @property
    def days_until_due(self):
        """
        Кількість днів до дедлайну
        """
        if not self.due_date:
            return None
        
        delta = self.due_date - timezone.now()
        return delta.days
    
    @property
    def duration(self):
        """
        Тривалість роботи над завданням
        """
        if not self.started_at:
            return None
            
        end_time = self.completed_at or timezone.now()
        return end_time - self.started_at
    
    @property
    def time_estimate_accuracy(self):
        """
        Точність оцінки часу (якщо є і оцінений, і фактичний час)
        """
        if not self.estimated_hours or not self.actual_hours:
            return None
        
        if self.estimated_hours == 0:
            return None
            
        accuracy = (self.actual_hours / self.estimated_hours) * 100
        return round(accuracy, 2)
    
    def get_tags_list(self):
        """
        Повертає список тегів
        """
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def add_tag(self, tag):
      pass
    
    def remove_tag(self, tag):
        """
        Видаляє тег
        """
        tags_list = self.get_tags_list()
        if tag in tags_list:
            tags_list.remove(tag)
            self.tags = ', '.join(tags_list)
    
    # TODO: Методи для роботи з підзавданнями
    # def get_subtasks(self):
    #     """Отримати всі підзавдання"""
    #     return self.subtasks.all()
    # 
    # def get_completion_percentage(self):
    #     """Розрахувати відсоток виконання з урахуванням підзавдань"""
    #     pass
    
    # TODO: Методи для роботи з часом
    # def start_timer(self):
    #     """Почати відлік часу роботи"""
    #     pass
    # 
    # def stop_timer(self):
    #     """Зупинити відлік часу роботи"""
    #     pass
    
class TaskCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        help_text='зберігання назви категорії завдань'
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="Детальний опис категорії"
    )

    colour = models.CharField(
        max_length=7,
        default="#007bff",
        null=True,
        blank=True,
        help_text="HEX колір (наприклад, #FF0000) для візуального відображення"
    )

    active = models.BooleanField(
        default=True,
        help_text="Визначатимите, чи є категорія активною для використання"
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Відстежування часу створення категорії"
        )
    class Meta:
        verbose_name = "Категорія завдань"
        verbose_name_plural = "Категорії завдань"
        ordering = ["назва"]  # сортування по алфавіту

    def __str__(self):
        return self.назва
