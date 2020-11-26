from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_banned = models.BooleanField(default=False)


class Room(models.Model):
    """Модель комнаты чата"""
    creator = models.ForeignKey(User, verbose_name="Участники", related_name="creator", on_delete=models.CASCADE)
    joiner = models.ForeignKey(User, related_name='joiner', on_delete=models.CASCADE)
    date = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Комната чата"
        verbose_name_plural = "Комнаты чатов"


class Chat(models.Model):
    """Модель чата"""
    room = models.ForeignKey(Room, verbose_name="Комната чата", related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чатов"
