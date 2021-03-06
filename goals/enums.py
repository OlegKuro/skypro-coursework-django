from django.db import models


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"

class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class BoardRole(models.IntegerChoices):
    owner = 1, "Владелец"
    writer = 2, "Редактор"
    reader = 3, "Читатель"

    @classmethod
    @property
    def editable_choices(cls):
        choices = cls.choices
        cls.choices.pop(0)
        return choices
