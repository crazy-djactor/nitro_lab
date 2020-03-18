# Generated by Django 2.2.7 on 2019-11-25 05:47

import pos.storage_backends
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField()),
                ('pressure', models.FloatField()),
                ('humidity', models.FloatField()),
                ('image_file', models.FileField(storage=pos.storage_backends.PrivateMediaStorage(), upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
