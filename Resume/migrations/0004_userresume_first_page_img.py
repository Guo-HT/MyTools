# Generated by Django 2.1.15 on 2021-12-29 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Resume', '0003_auto_20211229_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresume',
            name='first_page_img',
            field=models.TextField(blank=True, default='', max_length=20, null=True, verbose_name='简历封面'),
        ),
    ]
