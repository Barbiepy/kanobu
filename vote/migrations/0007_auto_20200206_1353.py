# Generated by Django 3.0.3 on 2020-02-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_auto_20200206_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='votes',
            field=models.ManyToManyField(blank=True, related_name='comments', to='vote.Vote', verbose_name='Оценки'),
        ),
    ]