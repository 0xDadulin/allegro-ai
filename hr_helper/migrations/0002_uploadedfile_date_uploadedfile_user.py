# Generated by Django 4.1.7 on 2023-03-12 17:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("hr_helper", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadedfile",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(
                    2023, 3, 12, 17, 50, 3, 256141, tzinfo=datetime.timezone.utc
                ),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="uploadedfile",
            name="user",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]