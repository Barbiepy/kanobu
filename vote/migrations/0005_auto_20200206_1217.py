# Generated by Django 3.0.3 on 2020-02-06 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_vote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='status',
            field=models.CharField(choices=[('like', 'Понравилось'), ('dislike', 'Не понравилось')], max_length=7, verbose_name='Статус'),
        ),
    ]
