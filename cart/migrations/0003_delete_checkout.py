# Generated by Django 5.0.7 on 2024-07-21 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_checkout'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Checkout',
        ),
    ]