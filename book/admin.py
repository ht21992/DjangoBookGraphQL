from django.contrib import admin
from book.models import Book, Author,Genre,Character

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Character)
