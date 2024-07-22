# Generated by Django 5.0.7 on 2024-07-21 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_checkout_status'),
        ('order', '0002_remove_order_checkout_order_checkouts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='checkouts',
            field=models.ManyToManyField(related_name='orders', to='cart.checkout'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('COD', 'COD'), ('bank_transfer', 'Bank Transfer')], default='COD', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('delivered', 'Delivered')], default='draft', max_length=10),
        ),
    ]
