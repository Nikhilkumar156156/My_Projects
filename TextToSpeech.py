import pyttsx3

engine = pyttsx3.init()
print("Welcome to speaker Created By Nikhil")

while True:
    x = input("Enter what you want me to speak ('q' to quit): ")
    if x.lower() == 'q':
        break
    engine.say(x)
    engine.runAndWait()
