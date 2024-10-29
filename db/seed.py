import json
from datetime import datetime

from mongoengine import NotUniqueError, ValidationError, DoesNotExist

from db import connect_db
from models import Author, Quote


def fill_data():
    #  Fill authors
    with open("../authors.json") as f:
        data_from_file = json.load(f)
        for el in data_from_file:
            try:
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=datetime.strptime(el.get("born_date"), "%B %d, %Y"),
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )
                author.save()
                print(f"Created author: {author.id}")
            except ValidationError as e:
                print(f"Validation Error: {e}")
            except NotUniqueError as e:
                print(f"NotUnique Error: {e}")
    # Fill quotes
    with open("../quotes.json") as f:
        data_from_file = json.load(f)
        for el in data_from_file:
            try:
                author = Author.objects.get(fullname=el.get("author"))
                quote = Quote(
                    tags=el.get("tags"),
                    author=author,
                    quote=el.get("quote"),
                )
                quote.save()
                print(f"Created quote: {quote.id}")
            except ValidationError as e:
                print(f"Validation Error: {e}")
            except DoesNotExist as e:
                print(e, author.fullname)



if __name__ == "__main__":
    connect_db()
    fill_data()
