# Generated by Django 2.0.5 on 2018-10-14 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_article_audio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='audio',
        ),
        migrations.AddField(
            model_name='article',
            name='audio_filename',
            field=models.TextField(blank=True, null=True),
        ),
    ]
