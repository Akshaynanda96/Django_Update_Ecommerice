# Generated by Django 5.0.6 on 2024-06-07 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_color_variations_size_variations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color_variations',
            name='color_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='size_variations',
            name='Size_price',
            field=models.IntegerField(default=0),
        ),
    ]
