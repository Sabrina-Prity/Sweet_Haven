# Generated by Django 5.1.3 on 2025-01-05 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_to_cart', '0007_rename_orderdirectly_order_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]