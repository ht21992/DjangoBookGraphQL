# Generated by Django 5.1.2 on 2024-10-31 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0001_initial"),
        ("warehouse", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shelf",
            name="books",
            field=models.ManyToManyField(related_name="books", to="book.book"),
        ),
    ]
