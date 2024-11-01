from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=100)


class Shelf(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    books = models.ManyToManyField("book.Book", related_name="books")

