# Generated by Django 5.0.7 on 2024-07-21 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_checkout_checkoutitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('ordered', 'ordered')], default='pending', max_length=200),
        ),
    ]
