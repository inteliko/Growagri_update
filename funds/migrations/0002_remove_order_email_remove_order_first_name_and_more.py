# Generated by Django 5.0.4 on 2024-04-22 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
    ]
