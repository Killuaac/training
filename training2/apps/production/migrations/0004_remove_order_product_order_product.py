# Generated by Django 5.0.3 on 2024-04-11 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_alter_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='production.product'),
        ),
    ]
