from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author
from django.http import JsonResponse, HttpResponse
from graphql_bookstore.schema import schema
import json
import time
import uuid
from decimal import Decimal

# # Create a new book
# def create_book(request):
#     if request.method == "POST":
#         title = request.POST.get("title")
#         author_id = request.POST.get("author_id")
#         author = get_object_or_404(Author, id=author_id)
#         Book.objects.create(title=title, author=author)
#         return JsonResponse({"message": "Book created successfully"})
#     authors = Author.objects.all()
#     return render(request, "books/create_book.html", {"authors": authors})


def create_book(request):
    if request.method == "POST":
        body = json.loads(request.body)
        title = body.get("title")
        author_id = body.get("author_id")

        mutation = f"""
        mutation {{
          createBook(title: "{title}", authorId: {int(author_id)}) {{
            book {{
              id
              title
              author {{
                name
              }}
            }}
          }}
        }}
        """

        result = schema.execute(mutation)

        if result.errors:
            return JsonResponse(
                {"errors": [str(error) for error in result.errors]}, status=400
            )

        return JsonResponse(
            {
                "message": "Book created successfully",
                "book": result.data["createBook"]["book"],
            }
        )

    authors = Author.objects.all()
    return render(request, "books/create_book.html", {"authors": authors})


# Update an existing book
# def update_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     if request.method == "POST":
#         title = request.POST.get("title")
#         if title:
#             book.title = title
#             book.save()
#             return JsonResponse({"message": "Book updated successfully"})
#     return render(request, "books/update_book.html", {"book": book})

def update_book(request, book_id):
    if request.method == "POST":
        body = json.loads(request.body)

        title = body.get("title")
        publisher = body.get("publisher")
        series = body.get("series")
        language = body.get("language")
        isbn = body.get("isbn")
        description = body.get("description")
        rating = body.get("rating")
        pages = body.get("pages")
        price = body.get("price")
        image = body.get("image")
        gener_ids = body.get("gener_ids", [])
        character_ids = body.get("character_ids", [])

        if title and str(book_id) == str(book_id):
            # Convert to Decimal for price and rating
            price = str(price) if price is not None else None
            rating = str(rating) if rating is not None else None

            # Escape the title and other fields as necessary
            title = title.replace('"', '\\"') if title else None
            publisher = publisher.replace('"', '\\"') if publisher else None
            series = series.replace('"', '\\"') if series else None
            language = language.replace('"', '\\"') if language else None
            isbn = isbn.replace('"', '\\"') if isbn else None
            description = description.replace('"', '\\"') if description else None
            image = image.replace('"', '\\"') if image else None

            # Create mutation string
            mutation = f"""
            mutation {{
                updateBook(bookId: "{book_id}", title: "{title}", publisher: "{publisher}", series: "{series}",
                            language: "{language}", isbn: "{isbn}", description: "{description}",
                            rating: {rating}, pages: {pages}, price: {price}, image: "{image}",
                            generIds: {json.dumps(gener_ids)}, characterIds: {json.dumps(character_ids)}) {{
                    book {{
                        id
                        title
                        publisher
                        series
                        language
                        isbn
                        description
                        rating
                        pages
                        price
                        image
                    }}
                }}
            }}
            """

            result = schema.execute(mutation)

            if result.errors:
                return JsonResponse(
                    {"errors": [str(error) for error in result.errors]}, status=400
                )

            return JsonResponse(
                {
                    "message": "Book updated successfully",
                    "book": result.data["updateBook"]["book"],
                }
            )

        return JsonResponse({"errors": ["Title cannot be empty"]}, status=400)

    book = get_object_or_404(Book, id=book_id)
    return render(request, "books/update_book.html", {"book": book})



# Delete a book
# def delete_book(request, book_id):
#     # 0.007680899929255247
#     # Pros : Simplicity , Direct interaction,  Faster response
#     # Cons : Limited flexibility , Less scalable for complex operations that involve multiple entities
#     start = time.perf_counter()
#     book = get_object_or_404(Book, id=book_id)
#     if request.method == "POST":

#         book.delete()
#         end = time.perf_counter()
#         print(end - start)
#         return JsonResponse({"message": "Book deleted successfully"})
#     return render(request, "books/delete_book.html", {"book": book})


def delete_book(request, book_id):
    # 0.02026649983599782
    """
    Pros:
        Flexibility: GraphQL allows for more complex interactions and can handle nested queries easily.
        Single endpoint: You can manage all CRUD operations through a single GraphQL endpoint, making the API more cohesive.
        Strong typing and introspection: Easier to manage data types and relationships between entities.

    Cons:
        Complexity: Requires understanding GraphQL and its syntax.
        Performance: Might be slightly slower due to the overhead of executing a GraphQL query.
    """
    if request.method == "POST":
        start = time.perf_counter()
        mutation = f"""
        mutation {{
            deleteBook(bookId: "{uuid.UUID(book_id)}") {{
                success
            }}
        }}
        """

        result = schema.execute(mutation)

        if result.errors:
            return JsonResponse(
                {"errors": [str(error) for error in result.errors]}, status=400
            )
        end = time.perf_counter()
        print(end - start)
        return JsonResponse({"message": "Book deleted successfully"})

    book = get_object_or_404(Book, id=book_id)
    return render(request, "books/delete_book.html", {"book": book})


def fetch_books_from_graphql(request):
    limit = 10
    offset = int(request.GET.get("offset", 0))
    jsResp = request.GET.get("jsResp", 0)
    query = """
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
    """

    variables = {"limit": limit, "offset": offset}

    result = schema.execute(query, variables=variables)

    if result.errors:
        return HttpResponse("Error fetching data", status=400)

    books = result.data["allBooks"]

    if int(jsResp):
        return JsonResponse({"books": books}, status=200)

    return render(request, "books/book_list.html", {"books": books})
