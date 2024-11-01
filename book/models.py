from django.db import models
from uuid import uuid4
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)


class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Authors"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Geners"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Characters"
        ordering = ("name",)

    def __str__(self):
        return self.name


# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=500, blank=False, verbose_name="title")
    author = models.ForeignKey(Author, related_name="books",null=False, on_delete=models.CASCADE)
    publisher = models.CharField(max_length=500, blank=True, verbose_name="publisher")
    series = models.CharField(max_length=500, blank=True, verbose_name="series")
    language = models.CharField(max_length=500, blank=True, verbose_name="language")

    isbn = models.CharField(max_length=500, blank=True, verbose_name="isbn")
    description = models.TextField(verbose_name="description", blank=True, default="No Desc")

    geners = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name="geners",
        related_name="books"
    )

    characters = models.ManyToManyField(
        Character,
        blank=True,
        verbose_name="characters",
        related_name="books"
    )
    rating = models.FloatField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
    )
    pages = models.IntegerField(default=0, blank=True)
    price = models.DecimalField(blank=True, max_digits=19, decimal_places=2, null=True)
    image = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "book"
        verbose_name_plural = "books"
        ordering = ("title",)

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
