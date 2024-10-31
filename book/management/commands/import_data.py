import pandas as pd
from django.core.management.base import BaseCommand
from book.models import Book, Genre, Character, Author
import ast
import decimal

# "python manage.py import_data path/to/your/data.csv"
# "python manage.py import_data booksDataSet.csv"


class Command(BaseCommand):
    help = "Import data from CSV file into the database"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def is_decimal(self, number):
        try:
            decimal_number = decimal.Decimal(str(number))
            return True
        except Exception:
            return False

    def convert_to_list(self, ls):
        try:
            converted = ast.literal_eval(ls)
            if isinstance(converted, list):
                return converted
            else:
                return []
        except (SyntaxError, ValueError):
            print(
                "Invalid input. Unable to convert to a list.returned empty list instead"
            )
            return []

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            for _, row in df.iterrows():

                if not Book.objects.filter(isbn=row["isbn"]).exists():
                    # Create the book
                    book = Book()
                    author, created = Author.objects.get_or_create(name=row["author"])
                    book.title = row["title"]
                    book.author = author
                    book.publisher = row["publisher"]
                    book.description = row["description"]
                    if pd.notna(row["series"]):
                        book.series = row["series"].split("#")[0]
                    book.language = row["language"]
                    book.isbn = row["isbn"]
                    if pd.notna(row["rating"]):
                        book.rating = row["rating"]
                    if pd.notna(row["pages"]):
                        if str(row["pages"]).strip() == "1 page":
                            book.pages = 1
                        else:
                            book.pages = row["pages"]
                    if pd.notna(row["price"]) and self.is_decimal(row["price"]):
                        book.price = row["price"]
                    book.image = row["coverImg"]
                    book.save()

                    for genre_name in self.convert_to_list(row["genres"]):
                        # Check if the genre already exists or create it
                        genre, created = Genre.objects.get_or_create(name=genre_name)
                        # Add the genre to the book's ManyToMany field
                        book.geners.add(genre)

                    for character_name in self.convert_to_list(row["characters"]):
                        # Check if the genre already exists or create it
                        character, created = Character.objects.get_or_create(
                            name=character_name
                        )
                        # Add the genre to the book's ManyToMany field
                        book.characters.add(character)
                    self.stdout.write(self.style.SUCCESS(f"{row['title']} added"))
            self.stdout.write(self.style.SUCCESS("Data import successful."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("CSV file not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
