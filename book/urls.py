from django.urls import path
from . import views

urlpatterns = [
    path('books/create/', views.create_book, name='create_book'),
    path('books/update/<int:book_id>/', views.update_book, name='update_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('books/', views.fetch_books_from_graphql, name='fetch_books'),
]