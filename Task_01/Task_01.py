

import requests
import os

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
            "temperature": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "weather": data.get("weather", [{}])[0].get("main")
        }
        return result
    except requests.RequestException as e:
        print(f"Error fetching weather data for {city_name}: {e}")
        return None


def main():
    cities_input = input("Enter city names separated by commas (e.g., London, Paris, New York): ").strip()
    cities = [city.strip() for city in cities_input.split(",")]
    weather_data_list = []
    for city in cities:
        weather_data = get_weather(city)
        if weather_data:
            weather_data_list.append(weather_data)

    if not weather_data_list:
        print("No weather data retrieved. Exiting.")
        return

    if len(weather_data_list) == 1:
        data = weather_data_list[0]
        print(f"\nWeather Data for {data['city']}, {data['country']}:")
        print(f"Temperature: {data['temperature']}°C")
        print(f"Humidity: {data['humidity']}%")
        print(f"Weather: {data['weather']}")
    else:
        print("\nWeather Data for Entered Cities:")
        for data in weather_data_list:
            print(f"\nCity: {data['city']}, {data['country']}")
            print(f"Temperature: {data['temperature']}°C")
            print(f"Humidity: {data['humidity']}%")
            print(f"Weather: {data['weather']}")

        temperatures = [data['temperature'] for data in weather_data_list]
        average_temp = sum(temperatures) / len(temperatures)
        coldest_city = min(weather_data_list, key=lambda x: x['temperature'])

        print("\nStatistics:")
        print(f"Average Temperature: {average_temp:.2f}°C")
        print(f"Coldest City: {coldest_city['city']} ({coldest_city['temperature']}°C)")


if __name__ == "__main__":
    main()