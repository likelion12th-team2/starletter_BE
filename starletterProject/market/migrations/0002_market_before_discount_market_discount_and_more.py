# Generated by Django 4.2.14 on 2024-07-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='before_discount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='discount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
