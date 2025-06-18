import requests
import json

query=input("what type of news you want?:")
url=f"https://newsapi.org/v2/everything?q={query}&from=2025-05-05&sortBy=publishedAt&apiKey=d727fcd0699d4a79accbb2b85d2416c4"

r=requests.get(url)
news=json.loads(r.text)

for article in news["articles"]:
    print(article["title"])
    print(article["description"])
    print("---------------------")
