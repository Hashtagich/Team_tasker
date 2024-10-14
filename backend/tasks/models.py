from django.db import models
from users.models import CustomUser


# Create your models here.

class Task(models.Model):
    """Модель задачи."""
    CHOICE_STATUS = (
        ('new', 'новая'),
        ('in_work', 'в работе'),
        ('done', 'завершена')
    )

    name = models.CharField(
        verbose_name='Название',
        max_length=30,
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=CHOICE_STATUS,
        default="new",
        blank=True
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='task_author',
        verbose_name='Автор'
    )

    implementer = models.ForeignKey(
        CustomUser,
        verbose_name='Исполнитель',
        on_delete=models.CASCADE,
        related_name='task_implementer',
        null=True,
        blank=True
    )

    datetime_start = models.DateTimeField(
        verbose_name="Дата начала задачи",
        blank=True,
        null=True
    )

    datetime_finish_plan = models.DateTimeField(
        verbose_name="Дата выполнения задачи - План",
        blank=True,
        null=True
    )

    datetime_finish_fact = models.DateTimeField(
        verbose_name="Дата выполнения задачи - Факт",
        blank=True,
        null=True
    )

    datetime_create = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    datetime_update = models.DateTimeField(
        verbose_name='Дата редактирования',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('datetime_start',)

    def __str__(self):
        return f'{self.name}'
