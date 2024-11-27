from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)


API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        result = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": round(data.get("main", {}).get("temp"), 1),
            "humidity": data.get("main", {}).get("humidity"),
            "weather": data.get("weather", [{}])[0].get("main")
        }
        return result
    except requests.RequestException as e:
        print(f"Error fetching weather data for {city_name}: {e}")
        return None

def calculate_statistics(weather_data_list):
    temperatures = [data['temperature'] for data in weather_data_list]
    average_temp = sum(temperatures) / len(temperatures)
    coldest_city = min(weather_data_list, key=lambda x: x['temperature'])

    return average_temp, coldest_city

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather_data():
    cities_input = request.form['cities']
    cities = [city.strip() for city in cities_input.split(",")]

    weather_data_list = []
    for city in cities:
        weather_data = get_weather(city)
        if weather_data:
            weather_data_list.append(weather_data)

    if not weather_data_list:
        return jsonify({"error": "Could not retrieve weather data."}), 400

    if len(weather_data_list) > 1:
        avg_temp, coldest_city = calculate_statistics(weather_data_list)
        statistics = {
            "average_temp": round(avg_temp, 1),
            "coldest_city": coldest_city['city']
        }
    else:
        statistics = {}

    return jsonify({"weather_data": weather_data_list, "statistics": statistics})

if __name__ == '__main__':
    app.run(debug=True)