# Generated by Django 3.0.9 on 2023-09-27 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_informed',
            field=models.BooleanField(default=False),
        ),
    ]
