# Generated by Django 4.2.2 on 2023-06-27 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_rename_freatured_image_product_big_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_info',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='add_info',
            name='color',
        ),
        migrations.RemoveField(
            model_name='add_info',
            name='dimensions',
        ),
        migrations.RemoveField(
            model_name='add_info',
            name='size',
        ),
        migrations.RemoveField(
            model_name='add_info',
            name='weight',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='dimensions',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
