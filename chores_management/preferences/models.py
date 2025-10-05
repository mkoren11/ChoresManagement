from django.db import models
from .models import User


class UserPreferences(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="preferences",
        verbose_name="Користувач"
    )
    liked_categories = models.ManyToManyField(
        "Category",
        related_name="liked_by_users",
        blank=True,
        verbose_name="Улюблені категорії"
    )
    disliked_categories = models.ManyToManyField(
        "Category",
        related_name="disliked_by_users",
        blank=True,
        verbose_name="Неулюблені категорії"
    )
    availability = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Доступність"
    )
    experience_levels = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Рівень досвіду"
    )
    physical_limitations = models.TextField(
        blank=True,
        verbose_name="Фізичні обмеження"
    )

    class Meta:
        verbose_name = "Налаштування користувача"
        verbose_name_plural = "Налаштування користувачів"

    def __str__(self):
        return f"Налаштування користувача {self.user.username}"
    
