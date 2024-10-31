from django.urls import path
from . import views

urlpatterns = [
    path('books/create/', views.create_book, name='create_book'),
    path('books/update/<str:book_id>/', views.update_book, name='update_book'),
    path('books/delete/<str:book_id>/', views.delete_book, name='delete_book'),
    path('', views.fetch_books_from_graphql, name='fetch_books'),
]
