# Generated by Django 5.1.2 on 2024-10-31 05:36

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "Authors",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Character",
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
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Characters",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Geners",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=500, verbose_name="title")),
                (
                    "publisher",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="publisher"
                    ),
                ),
                (
                    "series",
                    models.CharField(blank=True, max_length=500, verbose_name="series"),
                ),
                (
                    "language",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="language"
                    ),
                ),
                (
                    "isbn",
                    models.CharField(blank=True, max_length=500, verbose_name="isbn"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="No Desc", verbose_name="description"
                    ),
                ),
                (
                    "rating",
                    models.FloatField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                ("pages", models.IntegerField(blank=True, default=0)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=19, null=True
                    ),
                ),
                ("image", models.URLField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="book.author",
                    ),
                ),
                (
                    "characters",
                    models.ManyToManyField(
                        blank=True, to="book.character", verbose_name="characters"
                    ),
                ),
                (
                    "geners",
                    models.ManyToManyField(
                        blank=True,
                        related_name="geners",
                        to="book.genre",
                        verbose_name="geners",
                    ),
                ),
            ],
            options={
                "verbose_name": "book",
                "verbose_name_plural": "books",
                "ordering": ("-updated",),
            },
        ),
    ]
