# Generated by Django 5.0.6 on 2024-05-26 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PerevalAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=255, verbose_name='Индекс')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('other_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Другое название')),
                ('connect', models.TextField(blank=True, null=True, verbose_name='Соединяет')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('status', models.CharField(choices=[('new', 'New'), ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='new', max_length=8, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Перевал',
                'verbose_name_plural': 'Перевалы',
            },
        ),
        migrations.CreateModel(
            name='PerevalCoordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('height', models.IntegerField(verbose_name='Высота')),
            ],
            options={
                'verbose_name': 'Координаты',
                'verbose_name_plural': 'Координаты',
            },
        ),
        migrations.CreateModel(
            name='PerevalLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(blank=True, choices=[('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('4a', '4А'), ('4b', '4Б'), ('5a', '5А'), ('5b', '5Б')], max_length=2, null=True, verbose_name='Зима')),
                ('spring', models.CharField(blank=True, choices=[('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('4a', '4А'), ('4b', '4Б'), ('5a', '5А'), ('5b', '5Б')], max_length=2, null=True, verbose_name='Весна')),
                ('summer', models.CharField(blank=True, choices=[('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('4a', '4А'), ('4b', '4Б'), ('5a', '5А'), ('5b', '5Б')], max_length=2, null=True, verbose_name='Лето')),
                ('autumn', models.CharField(blank=True, choices=[('1a', '1A'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('4a', '4А'), ('4b', '4Б'), ('5a', '5А'), ('5b', '5Б')], max_length=2, null=True, verbose_name='Осень')),
            ],
            options={
                'verbose_name': 'Уровень',
                'verbose_name_plural': 'Уровни',
            },
        ),
        migrations.CreateModel(
            name='PerevalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('otc', models.CharField(max_length=255, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('phone', models.CharField(max_length=11, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('data', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pereval.perevaladded', verbose_name='Перевал')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='coord',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pereval', to='pereval.perevalcoordinate', verbose_name='Координаты'),
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perevals', to='pereval.perevallevel', verbose_name='Уровень'),
        ),
        migrations.AddConstraint(
            model_name='perevaluser',
            constraint=models.UniqueConstraint(fields=('email',), name='unique_email'),
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perevals', to='pereval.perevaluser', verbose_name='Пользователь'),
        ),
    ]