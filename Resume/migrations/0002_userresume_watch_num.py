# Generated by Django 2.1.15 on 2021-12-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresume',
            name='watch_num',
            field=models.IntegerField(default=0, verbose_name='浏览量'),
        ),
    ]