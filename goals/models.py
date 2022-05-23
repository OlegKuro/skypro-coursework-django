from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.postgres.indexes import HashIndex

from core.models import User
from goals.enums import Status, Priority, BoardRole


class HasCreatedUpdatedFieldsMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class HasAuthorMixin(models.Model):
    class Meta:
        abstract = True
        indexes = (
            HashIndex(fields=('user',)),
        )

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)


class GoalCategory(HasCreatedUpdatedFieldsMixin, HasAuthorMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(to='Board', verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class Goal(HasCreatedUpdatedFieldsMixin, HasAuthorMixin):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(to=GoalCategory, related_name='goals', related_query_name='goals',
                                 verbose_name='Категория', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )


class GoalComment(HasCreatedUpdatedFieldsMixin, HasAuthorMixin):
    goal = models.ForeignKey(to=Goal, on_delete=models.CASCADE, related_name='comments', related_query_name='comments',
                             verbose_name='Цель')
    text = models.TextField(validators=[MinLengthValidator(1)])


class Board(HasCreatedUpdatedFieldsMixin):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(HasCreatedUpdatedFieldsMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=BoardRole.choices, default=BoardRole.owner
    )