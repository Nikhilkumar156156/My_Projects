import requests
import json
import pyttsx3

API_KEY = "1a0a97b65a83454a9fdf2b5fca257a10"

engine = pyttsx3.init()
engine.setProperty('rate', 165)

engine.say("Welcome, Here are the top five news headlines")
engine.runAndWait()

query = input("What type of news do you want? : ")

url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
response = requests.get(url)
news = json.loads(response.text)

if news["status"] != "ok":
    print("Failed to fetch news.")
    engine.say("Sorry, I could not fetch the news.")
    engine.runAndWait()
    exit()

print("\nTop 5 News:\n")

for i, article in enumerate(news["articles"][:5], start=1):
    title = article["title"]
    description = article["description"] or "Description not available."

    print(f"{i}. {title}")
    print(description)
    print("-" * 40)

    engine.say(title)
    engine.runAndWait()
    engine.stop()

    engine.say(description)
    engine.runAndWait()
    engine.stop()
