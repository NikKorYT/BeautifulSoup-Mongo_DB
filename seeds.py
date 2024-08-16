from mongoengine import connect
import configparser
from models import authors, qoutes
import json

# read config file for DB key safety
config = configparser.ConfigParser()
config.read("configs/config.ini")

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
domain = config.get("DB", "domain")


# reading and parsing json file for authors and saving to DB
def seed_authors():
    with open("contents/authors.json") as f:
        data = json.load(f)
        for author in data:
            author = authors(
                full_name=author["fullname"],
                born_date=author["born_date"],
                born_location=author["born_location"],
                description=author["description"],
            )
            author.save()


# same for quotes
def seed_qoutes():
    with open("contents/qoutes.json") as f:
        data = json.load(f)
        for quote in data:
            quote = qoutes(
                tags=quote["tags"],
                author=authors.objects(full_name=quote["author"]).first(),
                quote=quote["quote"],
            )
            quote.save()
            
def clear_db():
    authors.objects().delete()
    qoutes.objects().delete()
    print("DB cleared!")


if __name__ == "__main__":
    # check connection to DB
    try:
        connect(
            host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority""",
            ssl=True,
        )
        print("Connected to DB")
    except Exception as e:
        print("Error: ", e)

    # seed authors and qoutes
    try:
        clear_db()
        seed_authors()
        seed_qoutes()
        print("Seeding completed!")
    except Exception as e:
        print("Error: ", e)
