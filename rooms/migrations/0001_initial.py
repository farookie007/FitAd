# Generated by Django 4.1.7 on 2023-11-06 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import rooms.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=20)),
                (
                    "code",
                    models.CharField(
                        default=rooms.models.generate_code, max_length=10, unique=True
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "host",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
