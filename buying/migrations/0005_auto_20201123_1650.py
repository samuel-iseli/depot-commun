# Generated by Django 3.1.3 on 2020-11-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buying', '0004_auto_20201123_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='uuid',
        ),
        migrations.AddField(
            model_name='item',
            name='product_nr',
            field=models.PositiveSmallIntegerField(default=11, unique=True),
            preserve_default=False,
        ),
    ]
