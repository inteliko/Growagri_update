# Generated by Django 5.0.4 on 2024-04-24 18:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('author_name', models.CharField(max_length=100)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default='default.jpg', upload_to='post_images')),
            ],
        ),
    ]
