# Generated by Django 5.1.3 on 2025-01-01 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_buy_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Buy',
        ),
    ]