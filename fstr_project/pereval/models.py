from django.db import models
from .resources import *


class PerevalUser(models.Model):
    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    otc = models.CharField(max_length=255, verbose_name='Отчество')
    email = models.EmailField(unique=True, verbose_name='Почта')
    email = models.EmailField(max_length=255, verbose_name='Почта')
    phone = models.CharField(max_length=11, verbose_name='Телефон')

    def __str__(self):
        return f'{self.surname} {self.name} {self.otc}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        # constraints = [
        #     models.UniqueConstraint(fields=['email'], name='unique_email')
        # ]

class PerevalCoordinate(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def __str__(self):
        return f'широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}'

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"

class PerevalLevel(models.Model):
    winter = models.CharField(max_length=2, choices=level_list, verbose_name='Зима', null=True, blank=True)
    spring = models.CharField(max_length=2, choices=level_list, verbose_name='Весна', null=True, blank=True)
    summer = models.CharField(max_length=2, choices=level_list, verbose_name='Лето', null=True, blank=True)
    autumn = models.CharField(max_length=2, choices=level_list, verbose_name='Осень', null=True, blank=True)

    def __str__(self):
        l_winter = f'Зима - {self.winter};' if self.winter else ""
        l_summer = f'Лето - {self.summer};' if self.summer else ""
        l_autumn = f'Осень - {self.autumn};' if self.autumn else ""
        l_spring = f'Весна - {self.spring};' if self.spring else ""

        return f'{l_winter} {l_summer} {l_autumn} {l_spring}'

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"

class PerevalAdded(models.Model):
    beauty_title = models.CharField(max_length=255, verbose_name='Индекс')
    title = models.CharField(max_length=255, verbose_name='Название')
    other_title = models.CharField(max_length=255, verbose_name='Другое название', null=True, blank=True)
    connect = models.TextField(verbose_name='Соединяет', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.CharField(max_length=8, choices=status_choices, default=default_status, verbose_name='Статус')
    coord = models.OneToOneField(PerevalCoordinate, on_delete=models.CASCADE, verbose_name='Координаты', related_name='pereval')
    user = models.ForeignKey(PerevalUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='perevals')
    level = models.ForeignKey(PerevalLevel, on_delete=models.CASCADE, verbose_name='Уровень', related_name='perevals')

    def __str__(self):
        return f'{self.beauty_title}, {self.title}'

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевалы"

class Image(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    data = models.ImageField(upload_to='images/', verbose_name='Изображение', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    pereval = models.ForeignKey(PerevalAdded, related_name='images', on_delete=models.CASCADE, verbose_name='Перевал')

    def __str__(self):
        return self.title if self.title else 'Без названия'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
