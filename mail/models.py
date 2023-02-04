from django.db import models
from django.utils.datetime_safe import date

NULLABLE = {'blank': True, 'null': True}


class Customer(models.Model):
    email = models.CharField(max_length=150, verbose_name='Контактный email')
    name = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Sending(models.Model):
    PER_DAY = 'per day'
    PER_WEEK = 'per week'
    PER_MONTH = 'per month'
    PERIODS = (
        ('per day', 'раз в день'),
        ('per week', 'раз в неделю'),
        ('per month', 'раз в месяц'),
    )
    COMPLETED = 'completed'
    CREATED = 'created'
    LAUNCHED = 'launched'
    STATUSES = (
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
    )

    send_time = models.TimeField(verbose_name='Время рассылки', **NULLABLE)
    period = models.CharField(max_length=20, choices=PERIODS, default=PER_MONTH, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUSES, default=CREATED, verbose_name='Статус')
    start_date = models.DateField(default=date.today, verbose_name='Дата начала')
    finish_date = models.DateField(default=date.today, verbose_name='Дата окончания')
    customer_lst = models.ForeignKey('mail.Customer', verbose_name='Список клиентов', on_delete=models.SET_NULL, null=True)
    sending_msg = models.ForeignKey('mail.Message', verbose_name='Сообщение', on_delete=models.SET_NULL, null=True)



class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема сообщения', **NULLABLE)
    text = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.title


class Attempt(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=20, verbose_name='Статус попытки')
    answer = models.CharField(max_length=250, **NULLABLE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'