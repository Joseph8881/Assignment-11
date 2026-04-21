import os
import requests
import random
from django.shortcuts import render
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://172.31.42.244:27017/")
db = client["weatherDB"]
collection = db["history"]


def home(request):
    return render(request, "continent_form.html")


def results(request):
    if request.method == "POST":
        continent = request.POST.get("continent")

        url = f"https://restcountries.com/v3.1/region/{continent}"
        response = requests.get(url)
        countries = response.json()

        selected = random.sample(countries, 5)

        results = []
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")

        for country in selected:
            name = country.get("name", {}).get("common")
            capital = country.get("capital", ["N/A"])[0]

            weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={api_key}&units=metric"
            weather_res = requests.get(weather_url).json()

            temp = weather_res.get("main", {}).get("temp", "N/A")
            description = weather_res.get("weather", [{}])[0].get("description", "N/A")

            data = {
                "country": name,
                "capital": capital,
                "temp": temp,
                "desc": description
            }

            results.append(data)
            collection.insert_one(data)

        return render(request, "search_results.html", {"results": results})

    return render(request, "continent_form.html")


def history(request):
    records = list(collection.find())
    return render(request, "history.html", {"records": records})