import os
import keyboard
import pyautogui
import webbrowser
from time import sleep
from urllib.parse import quote
# import pyowm
# from pyowm.utils import timestamps
# from datetime import datetime
import subprocess
import wolframalpha
app_id = "R5G7P8-69QK2P28PK"
client = wolframalpha.Client(app_id=app_id)

# location = "Banbarad,India"

# open_weather_api_key='14db83cc45d773c50212aa030e74fc1a'
# owm = pyowm.OWM(open_weather_api_key)
# current_weather = owm.weather_manager()
# tomorrow = timestamps.tomorrow()

# weekday = datetime.today().weekday()
# current_date = datetime.today()


def visit_site(nameOfWeb):
    nameOfWeb = quote(nameOfWeb,safe='')
    url = f"https://www.{nameOfWeb}.com"
    webbrowser.open(url=url)
    return True


def search(engine,searchItem):
    searchItem = quote(searchItem,safe='')
    search_url = f"https://www.{engine}.com/search?q={searchItem}"
    webbrowser.open(search_url)
    return True


def open_app(app_name):
    try:
        subprocess.Popen([app_name])
        # print(f"Opening {app_name}...")
        return True
    except FileNotFoundError:
        # print(f"Error: {app_name} not found.")
        pyautogui.press("win")
        sleep(1)
        keyboard.write(app_name)
        keyboard.press("enter")
        sleep(0.5)
        return True



def currentWeather():
    res = client.query("current weather in bhilai")
    result = str(next(res.results).text).split(sep="\n")
    final = []
    for rs in result:
        temp = rs.split(sep="|")
        if temp[0]=='conditions ':
            final.append(temp[0]+temp[1])
        elif temp[0] == "temperature ":
            final.append(temp[0]+temp[1])
    return final


def weatherForecastOnSpeceficDay(day :str):
    res = client.query(f'weather in bhilai on {day}')
    return str(next(res.results).text).split(sep='\n')
    


def tomorrowsWeather():
    res = client.query('tomorrows weather in bhilai')
    return str(next(res.results).text).split(sep='\n')

