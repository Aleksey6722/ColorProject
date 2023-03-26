# Generated by Django 4.1.7 on 2023-03-24 04:21

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("name", models.CharField(max_length=30)),
                ("issue_date", models.DateField()),
            ],
            options={
                "db_table": "brand",
            },
        ),
        migrations.CreateModel(
            name="Car",
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
                ("model", models.CharField(max_length=30)),
                (
                    "brand",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="car",
                        to="core.brand",
                    ),
                ),
            ],
            options={
                "db_table": "car",
            },
        ),
        migrations.CreateModel(
            name="Color",
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
                ("color_name", models.CharField(max_length=6, unique=True)),
            ],
            options={
                "db_table": "color",
            },
        ),
        migrations.CreateModel(
            name="Country",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("locale", models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                "db_table": "country",
            },
        ),
        migrations.CreateModel(
            name="User",
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
                ("login", models.CharField(max_length=20, unique=True)),
                ("password", models.CharField(max_length=64)),
                ("name", models.CharField(max_length=64)),
                ("email", models.CharField(max_length=64, unique=True)),
                ("registration_date", models.BigIntegerField(default=1679631676)),
                ("last_signin_date", models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="Session",
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
                    "key",
                    models.CharField(default=core.models.key_generating, max_length=64),
                ),
                ("date", models.BigIntegerField(default=1679631676)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="session",
                        to="core.user",
                    ),
                ),
            ],
            options={
                "db_table": "session",
            },
        ),
        migrations.CreateModel(
            name="Favourite",
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
                ("date", models.BigIntegerField(default=1679631676)),
                (
                    "car",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="favourite",
                        to="core.car",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="favourite",
                        to="core.user",
                    ),
                ),
            ],
            options={
                "db_table": "favourite",
            },
        ),
        migrations.AddField(
            model_name="car",
            name="color",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="car",
                to="core.color",
            ),
        ),
        migrations.AddField(
            model_name="brand",
            name="country",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="brand",
                to="core.country",
            ),
        ),
    ]
