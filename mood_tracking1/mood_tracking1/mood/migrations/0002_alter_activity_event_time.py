# Generated by Django 5.0.4 on 2024-04-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity_event',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
