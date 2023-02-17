from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE,
                                     **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', verbose_name='Превью', **NULLABLE)
    date_create = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    views_num = models.IntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.title
