# Generated by Django 4.1.13 on 2023-12-22 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0003_rename_user_userprofile_user_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Chanel',
            new_name='Channel',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='chanel',
            new_name='channel',
        ),
    ]