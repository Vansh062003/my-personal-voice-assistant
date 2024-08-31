import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai

import music

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# News API key
newsapi_key = "696dd604c87a4c9c894705a47b399dad"

# OpenAI API key
openai.api_key = 'your_openai_api_key_here'

def speak(text):
    engine.say(text)
    engine.runAndWait()

def fetch_news():
    response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}")
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        for article in articles:
            speak(article.get('title', 'No title available'))
    else:
        speak("Failed to fetch news")

def process_command(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("http://google.com")
    elif "open facebook" in command:
        webbrowser.open("http://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in command:  # Corrected typo
        webbrowser.open("http://linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        # Replace with actual music dictionary or handling
        link = music.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found")
    elif "news" in command:
        fetch_news()
    else:
        # Let OpenAI handle the request
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=command,
            max_tokens=150
        )
        speak(response.choices[0].text.strip())

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            if command.lower() == "jarvis":
                speak("Yes, vansh how can I assist you?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio)
                process_command(command)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, there was a problem with the speech recognition service.")
        except Exception as e:
            print("An error occurred:", e)
