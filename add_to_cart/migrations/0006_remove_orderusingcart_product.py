# Generated by Django 5.1.3 on 2025-01-02 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('add_to_cart', '0005_rename_order_orderusingcart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderusingcart',
            name='product',
        ),
    ]