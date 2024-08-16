# use BeutifulSoup to scrape the data from the website https://quotes.toscrape.com/
# abd save data in json files in contents folder

import requests
from bs4 import BeautifulSoup
import json
import os


def get_quotes() -> list:
    # scrap through all the pages of website
    # get all the quotes ob this format:
    # {
    #     "tags": ["change", "deep-thoughts", "thinking", "world"],
    #     "author": "Albert Einstein",
    #     "quote": "'The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.'",
    # },
    quotes = []
    for page in range(1, 11):
        response = requests.get(f"https://quotes.toscrape.com/page/{page}/")
        soup = BeautifulSoup(response.text, "html.parser")
        quotes_divs = soup.find_all(class_="quote")
        for div in quotes_divs:
            quote = {
                "tags": [tag.text for tag in div.find_all(class_="tag")],
                "author": div.find(class_="author").text,
                "quote": div.find(class_="text").text,
            }
            quotes.append(quote)
    return quotes


if __name__ == "__main__":
    quotes = get_quotes()
    # save the data in json files in contents folder
    if not os.path.exists("contents"):
        os.mkdir("contents")
    with open("contents/quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)
