# Generated by Django 4.1.7 on 2023-11-06 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="host",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="room",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]