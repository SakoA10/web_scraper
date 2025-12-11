from bs4 import BeautifulSoup
import requests
import json
import csv

books_data = []

for page in range(1, 6):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.select_one("p.price_color").text
        relative_link = book.h3.a["href"]
        full_link = "https://books.toscrape.com/catalogue/" + relative_link

        books_data.append({
            "title": title,
            "price": price,
            "link": full_link
        })

with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books_data, f, indent=4, ensure_ascii=False)

with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    writer.writeheader()
    writer.writerows(books_data)

print(f"Scraped {len(books_data)} books from 5 pages")
print("Saved to books.csv and books.json")
