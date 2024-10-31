import graphene
from graphene_django.types import DjangoObjectType
from .models import Book, Author


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author

class BookType(DjangoObjectType):
    class Meta:
        model = Book

# Queries to retrieve books and authors
class Query1(graphene.ObjectType):
    all_books = graphene.List(BookType)
    all_authors = graphene.List(AuthorType)
    books_by_author = graphene.List(BookType, author_id=graphene.Int())

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_all_authors(root, info):
        return Author.objects.all()

    def resolve_books_by_author(root, info, author_id):
        return Book.objects.filter(author_id=author_id)

# Mutations to create, update, and delete books
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(root, info, title, author_id):
        author = Author.objects.get(id=author_id)
        book = Book.objects.create(title=title, author=author)
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.Int(required=True)
        title = graphene.String()

    book = graphene.Field(BookType)

    def mutate(root, info, book_id, title):
        book = Book.objects.get(id=book_id)
        if title:
            book.title = title
            book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, book_id):
        Book.objects.get(id=book_id).delete()
        return DeleteBook(success=True)

# Root mutation class
class Mutation1(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

# Root schema
# schema = graphene.Schema(query=Query1, mutation=Mutation)


"""

Query All Books

query {
  allBooks {
    title
    author {
      name
    }
  }
}



Query Books by Author

query {
  booksByAuthor(authorId: 1) {
    title
  }
}



Create a New Book


mutation {
  createBook(title: "The Silmarillion", authorId: 1) {
    book {
      title
      author {
        name
      }
    }
  }
}



Update a Book


mutation {
  updateBook(bookId: 1, title: "The Hobbit: Updated") {
    book {
      title
    }
  }
}



Delete a Book


mutation {
  deleteBook(bookId: 1) {
    success
  }
}


"""