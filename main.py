import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_authors(author_page_url: str) -> dict:
    response = requests.get(author_page_url)
    soup = BeautifulSoup(response.text, "lxml")
    author_dict = {
        "fullname": soup.find("h3", class_="author-title").text,
        "born_date": soup.find("span", class_="author-born-date").text,
        "born_location": soup.find("span", class_="author-born-location").text,
        "description": soup.find("div", class_="author-description").text.strip(),
    }
    return author_dict


def scrape_quotes(url: str) -> tuple:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    quotes_list = []
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    tags = soup.find_all("div", class_="tags")
    for i in range(len(quotes)):
        tagsforquote = tags[i].find_all("a", class_="tag")
        quote_dict = {
            "quote": quotes[i].text,
            "author": authors[i].text,
            "tags": [tquote.text for tquote in tagsforquote],
        }
        quotes_list.append(quote_dict)

    # Get Author info
    authors_list = []
    for i in authors:
        if i.text not in authors_list:
            about_url = i.find_next_sibling("a")["href"]
            author_page_url = "https://quotes.toscrape.com" + about_url
            scraped_authors = scrape_authors(author_page_url)
            authors_list.append(scraped_authors)

    # Check for next page
    next_button = soup.find("li", class_="next")
    next_page_url = None
    if next_button:
        next_page_url = next_button.find("a")["href"]
        next_page_url = "https://quotes.toscrape.com" + next_page_url

    return quotes_list, authors_list, next_page_url


def scrape_quotes_all_pages():
    base_url = "https://quotes.toscrape.com"
    current_url = base_url
    all_quotes = []
    all_authors = []

    while current_url:
        print(f"Scraping {current_url}...")
        quotes, authors, next_page_url = scrape_quotes(current_url)
        all_quotes.extend(quotes)
        all_authors.extend(authors)
        current_url = next_page_url  # Move to the next page

    # Save quotes to json
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(all_quotes, file, ensure_ascii=False, indent=4)

    # Save authors to json
    with open("authors.json", "w", encoding="utf-8") as file:
        json.dump(all_authors, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    start = time.time()
    scrape_quotes_all_pages()
    end = time.time()
    print(end - start)
