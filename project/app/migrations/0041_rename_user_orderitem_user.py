# Generated by Django 4.2.2 on 2023-07-10 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_orderitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='user',
            new_name='User',
        ),
    ]
