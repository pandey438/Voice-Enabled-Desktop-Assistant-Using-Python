import pyttsx3
import requests
import speech_recognition as sr
from decouple import config
from datetime import datetime
from conv import random_text
from random import choice
import keyboard
import os
import subprocess as sp
from online import find_my_ip,search_on_google,search_on_wikipedia,youtube,send_email,get_news,weather_forecast
from email.message import EmailMessage
import smtplib
from decouple import config
import imdb


EMAIL="pparmarth@outlook.com"
PASSWORD=""



engine = pyttsx3.init('sapi5') #microsoft speech rec api

engine.setProperty('rate', 130)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

USER = config('USER')
HOSTNAME = config('BOT')
def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop'.lower() in queri.lower() or 'exit'.lower() in queri.lower():
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir,take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri

def greet_me():
    hour = datetime.now().hour
    if(hour>=6) and (hour<12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USER}")
    if (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")

    speak(f"I am {HOSTNAME}. How may i help you?{USER}")

listening = False

def start_listening():
    global listening
    listening = True
    print("Started listening")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening")

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "How are you".lower() in query:
                speak("I am absolutely fine sir.What about you")
            elif "open command prompt".lower() in query:
                speak("Opening command prompt")
                os.system('start cmd')
            elif "open camera".lower() in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:',shell=True)


            elif "open notepad".lower() in query:
                speak("Opening Notepad for you sir")
                notepad_path = "C:/Users/pparm/Desktop/New Text Document.txt"
                os.startfile(notepad_path)

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today,sir")
                speak(get_news())
                speak("I am printing in on terminal sir")
                print(*get_news(),sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                c= requests.get(f"http://ip-api.com/json/{ip_address}").json()
                city=c["city"]
                speak(f"Getting weather report of your city {city}")
                weather,temp,feels_like=weather_forecast(city)
                speak(f"The current temperature is {temp},but it feels like {feels_like}")
                speak(f"Also the weather report  talks about {weather}")
                speak("I am printing weather info on screen")
                print(f"Discription:{weather}\nTemperature: {temp}\nFeels Like: {feels_like}")


            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                          f"The plot summary of movie is {plot}")
                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")







