# Script to search for citations by tag, author name, or a set of tags. The script is executed in an infinite loop and uses the usual input statement to accept commands in the following command:value format. Example:
# name: Steve Martin - find and return a list of all quotes by the author Steve Martin;
# tag:life - find and return a list of quotes for the tag life;
# tags:life,live - find and return a list of quotes that contain the life or live tags (note: no spaces between the life, live tags);
# exit - exit the script;

from mongoengine import connect
import configparser
from models import authors, qoutes


def request_cycle():
    while True:
        command = input("Enter command: ")
        if command == "exit":
            break
        elif command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            author = authors.objects(full_name=author_name).first()
            if author:
                quotes = qoutes.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
            else:
                print("Author not found")
        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = qoutes.objects(tags=tag)
            if quotes:
                for quote in quotes:
                    print(quote.quote)
            else:
                print("Quotes for this tag are not found")
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(",")
            quotes = qoutes.objects(tags__in=tags)
            if quotes:
                for quote in quotes:
                    print(quote.quote)
            else:
                print("Quotes for these tags are not found")
        else:
            print("Invalid command")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("configs/config.ini")

    mongo_user = config.get("DB", "user")
    mongodb_pass = config.get("DB", "pass")
    domain = config.get("DB", "domain")

    try:
        connect(
            host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority""",
            ssl=True,
        )
        print("Connected to DB")
    except Exception as e:
        print("Error: ", e)

    request_cycle()
