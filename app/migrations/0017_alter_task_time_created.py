# Generated by Django 4.2.8 on 2024-01-31 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_filestask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]