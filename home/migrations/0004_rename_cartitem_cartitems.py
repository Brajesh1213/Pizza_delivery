# Generated by Django 4.2.6 on 2023-11-04 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItem',
            new_name='CartItems',
        ),
    ]