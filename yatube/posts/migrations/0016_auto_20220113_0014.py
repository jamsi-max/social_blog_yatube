# Generated by Django 2.2.16 on 2022-01-13 00:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20220112_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('like', models.BooleanField()),
                ('user_ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='posts.Ip', verbose_name='Лайки')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='post_like', to='posts.Like'),
        ),
    ]
