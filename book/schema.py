import graphene
from graphene_django.types import DjangoObjectType
from .models import Book, Author, Genre, Character
from django.db.models import Count, Avg

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author

class GenreType(DjangoObjectType):
    class Meta:
        model = Genre

class CharacterType(DjangoObjectType):
    class Meta:
        model = Character

class BookType(DjangoObjectType):
    class Meta:
        model = Book

# Queries to retrieve books and authors
class Query1(graphene.ObjectType):
    all_books = graphene.List(BookType)
    all_authors = graphene.List(AuthorType)
    books_by_author = graphene.List(BookType, author_id=graphene.Int())

class GenreStatsType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    book_count = graphene.Int()
    avg_rating = graphene.Float()


# Queries to retrieve books, authors, genres, characters
class Query(graphene.ObjectType):
    all_books = graphene.List(BookType, limit=graphene.Int(), offset=graphene.Int())
    all_authors = graphene.List(AuthorType, limit=graphene.Int(), offset=graphene.Int())
    all_geners = graphene.List(GenreType,limit=graphene.Int(), offset=graphene.Int())
    all_characters = graphene.List(CharacterType,limit=graphene.Int(), offset=graphene.Int())

    books = graphene.List(
        BookType,
        title=graphene.String(),
        min_rating=graphene.Float(),
        max_price=graphene.Decimal(),
        genre_id=graphene.Int(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    books_by_author = graphene.List(BookType, author_id=graphene.Int())
    books_by_character = graphene.List(BookType, character_id=graphene.Int())

    genre_stats = graphene.List(GenreStatsType, order_by=graphene.String(), asc=graphene.Boolean(),limit=graphene.Int(), offset=graphene.Int())

    def resolve_all_characters(root, info,limit=None, offset=None):
        """resolver is a function that fetch the data for a specific field in a schema"""
        charactes = Character.objects.all()
        if limit is not None:
            charactes = charactes[offset:offset+limit]
        return charactes


    def resolve_all_geners(root, info,limit=None, offset=None):
        genres = Genre.objects.all()
        if limit is not None:
            genres = genres[offset:offset+limit]
        return genres

    def resolve_all_books(root, info, limit=None, offset=None):
        books = Book.objects.select_related("author").prefetch_related("characters","geners")
        if limit is not None:
            books = books[offset:offset+limit]
        return books

    def resolve_all_authors(root, info,limit=None, offset=None):
        authors = Author.objects.all()
        if limit is not None:
            authors = authors[offset:offset+limit]
        return authors

    def resolve_books(root, info, title=None, min_rating=None, max_price=None, genre_id=None, limit=None, offset=None):
        queryset = Book.objects.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if genre_id:
            queryset = queryset.filter(geners__id=genre_id)
        if limit is not None:
            queryset = queryset[offset:offset + limit]
        return queryset

    def resolve_books_by_author(root, info, author_id):
        return Book.objects.filter(author_id=author_id)

    def resolve_books_by_character(root, info, character_id):
        return Book.objects.filter(characters__id=character_id).select_related("author").prefetch_related("geners", "characters")

    def resolve_genre_stats(root, info, order_by = None, asc=True,limit=None, offset=None):
        queryset = Genre.objects.values('id','name').annotate(book_count=Count('books'), avg_rating=Avg('books__rating'))
        if order_by:
            order_by = f"{'' if asc else '-'}{order_by}"
            queryset = queryset.order_by(order_by)
        if limit is not None:
            queryset = queryset[offset:offset + limit]
        return queryset

# Mutations to create, update, and delete books
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)
        publisher = graphene.String()
        series = graphene.String()
        language = graphene.String()
        isbn = graphene.String()
        description = graphene.String()
        rating = graphene.Float()
        pages = graphene.Int()
        price = graphene.Decimal()
        image = graphene.String()
        gener_ids = graphene.List(graphene.Int)
        character_ids = graphene.List(graphene.Int)


    book = graphene.Field(BookType)

    def mutate(root, info, title, author_id, **kwargs):
        author = Author.objects.get(id=author_id)
        book = Book.objects.create(title=title, author=author,**kwargs)
        if 'gener_ids' in kwargs:
            book.geners.set(kwargs['gener_ids'])
        if 'character_ids' in kwargs:
            book.characters.set(kwargs['character_ids'])
        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.UUID(required=True)
        title = graphene.String()
        publisher = graphene.String()
        series = graphene.String()
        language = graphene.String()
        isbn = graphene.String()
        description = graphene.String()
        rating = graphene.Float()
        pages = graphene.Int()
        price = graphene.Decimal()
        image = graphene.String()
        gener_ids = graphene.List(graphene.Int)
        character_ids = graphene.List(graphene.Int)

    book = graphene.Field(BookType)

    def mutate(root, info, book_id, **kwargs):
        book = Book.objects.get(id=book_id)
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        if 'gener_ids' in kwargs:
            book.geners.set(kwargs['gener_ids'])
        if 'character_ids' in kwargs:
            book.characters.set(kwargs['character_ids'])
        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.UUID(required=True)

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


Query With Offset

query allBooks($limit: Int, $offset: Int) {
      allBooks(limit: $limit, offset: $offset) {
        id
        title
        image
        author {
          name
        }
      }
    }



query  {
      allBooks(limit: 10, offset: 0) {
        id
        title
        image
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
