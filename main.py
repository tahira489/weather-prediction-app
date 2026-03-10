from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "588a2cfc83fa43837b4c9d8729c1cad8"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather",methods=["POST"])
def get_weather():
    city = request.form.get("city")

    if not city or not validate_city_name(city):
        return render_template("index.html",error="please enter a valid city name")
    
    base_url ="http://api.openweathermap.org/data/2.5/weather"
    params={"q":city,"appid":API_KEY,"units":"metric"}
    response = requests.get(base_url, params = params)
    if response.status_code == 200:
        data=response.json() 
        weather = {"city": data["name"],
                   "description": data["weather"][0]["description"],
                   "temperature": data["main"]["temp"],
                   "humidity": data["main"]["humidity"],
                   "wind_speed": data["wind"]["speed"],
                   "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                   }
        return render_template("index.html",weather = weather)
    elif response.status_code == 404:
        return render_template("index.html",error="city not found.please check the name")
    else:
        return render_template("index.html", error ="Unable to fetch weather data at the moment")
    
def validate_city_name(city):
  city = city.strip()
  if len(city) < 2 or len(city) > 50:
    return False
  if not all(c.isalpha() or c.isspace() for c in city):
    return False
  return True
if __name__ =="__main__":
  app.run(debug=True)