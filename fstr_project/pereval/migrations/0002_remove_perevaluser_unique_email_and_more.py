# Generated by Django 5.0.6 on 2024-06-04 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='perevaluser',
            name='unique_email',
        ),
        migrations.AlterField(
            model_name='perevaluser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='Почта'),
        ),
    ]
