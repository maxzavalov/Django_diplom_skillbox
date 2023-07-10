from django.db import models


class Avatar(models.Model):
    """ Модель для хранения аватара пользователя"""

    src = models.ImageField(upload_to='my_auth/avatars/user_avatars',
                            default='my_auth/avatars/default.png',
                            verbose_name='Ссылка')
    alt = models.CharField(max_length=128, verbose_name='Описание')

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

