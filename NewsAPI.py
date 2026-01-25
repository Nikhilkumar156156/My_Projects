import requests
import json

query=input("what type of news you want?:")
url=f"https://newsapi.org/v2/everything?q={query}&from=2026-01-05&sortBy=publishedAt&apiKey=1a0a97b65a83454a9fdf2b5fca257a10"

r=requests.get(url)
news=json.loads(r.text)

for article in news["articles"]:
    print(article["title"])
    print(article["description"])
    print("---------------------")