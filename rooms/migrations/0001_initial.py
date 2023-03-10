# Generated by Django 4.1.7 on 2023-02-23 21:39

from django.db import migrations, models
import django.db.models.deletion
import rooms.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                (
                    "code",
                    models.CharField(
                        default=rooms.models.generate_code, max_length=8, unique=True
                    ),
                ),
                ("host", models.CharField(max_length=255, unique=True)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Requests",
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
                ("song_title", models.CharField(max_length=255)),
                ("artiste", models.CharField(max_length=255)),
                ("sender_ID", models.CharField(max_length=255)),
                ("sender_IP", models.CharField(max_length=255)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_requests",
                        to="rooms.room",
                    ),
                ),
            ],
        ),
    ]
