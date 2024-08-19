import requests
import wikipedia
import pywhatkit as kit #access google ,yt
from email.message import EmailMessage

def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    result=wikipedia.summary(query,sentences=2)
    return result

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False

def get_news():
    news_headline = []
    try:
        result = requests.get("https://newsapi.org/v2/everything?q=india&from=2024-03-12&sortBy=publishedAt&apiKey=f87ad4ef75ba4dee944ba8d5ff41d76f").json()
        if "articles" in result:
            articles = result["articles"]
            for article in articles:
                news_headline.append(article["title"])
    except Exception as e:
        print(f"Error occurred: {e}")
    return news_headline[:6]

def weather_forecast(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c376c192a585914fcfbec3bf0ac028cd&units=metric"
        print("API URL:", url)
        res = requests.get(url).json()
        print("API Response:", res)
        weather = res["weather"][0]["main"]
        temp = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        return weather, f"{temp}°C", f"{feels_like}°C"
    except KeyError:
        return "Unknown", "Unknown", "Unknown"
    except Exception as e:
        print("An error occurred:", e)
        return "Unknown", "Unknown", "Unknown"