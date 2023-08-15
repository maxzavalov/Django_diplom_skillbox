from django.contrib.auth.models import User
from django.db import models


def avatar_upload_path(instance, filename):
    return f"avatars/user_{instance.user.id}/{filename}"


class Profile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        default="avatars/default.png",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    email = models.EmailField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.fullName
