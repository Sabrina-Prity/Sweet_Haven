# Generated by Django 5.1.3 on 2025-01-01 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_post_comment_mango_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]