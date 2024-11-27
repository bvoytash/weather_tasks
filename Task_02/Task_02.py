import tkinter as tk
from tkinter import messagebox
import requests, os


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


def display_weather(weather_data_list):
    result_text.delete(1.0, tk.END)

    for data in weather_data_list:
        result_text.insert(tk.END, f"City: {data['city']}, {data['country']}\n")
        result_text.insert(tk.END, f"Temperature: {data['temperature']}°C\n")
        result_text.insert(tk.END, f"Humidity: {data['humidity']}%\n")
        result_text.insert(tk.END, f"Weather: {data['weather']}\n")
        result_text.insert(tk.END, "-"*50 + "\n")


def display_statistics(weather_data_list):
    temperatures = [data['temperature'] for data in weather_data_list]
    average_temp = sum(temperatures) / len(temperatures)
    coldest_city = min(weather_data_list, key=lambda x: x['temperature'])

    stats_text.delete(1.0, tk.END)

    stats_text.insert(tk.END, f"Average Temperature: {average_temp:.2f}°C\n")
    stats_text.insert(tk.END, f"Coldest City: {coldest_city['city']} ({coldest_city['temperature']}°C)\n")


def fetch_weather():
    cities_input = city_entry.get().strip()
    cities = [city.strip() for city in cities_input.split(",")]

    weather_data_list = []
    for city in cities:
        weather_data = get_weather(city)
        if weather_data:
            weather_data_list.append(weather_data)

    if not weather_data_list:
        messagebox.showerror("Error", "Could not retrieve weather data.")
        return

    display_weather(weather_data_list)

    if len(weather_data_list) > 1:
        display_statistics(weather_data_list)
    else:
        stats_text.delete(1.0, tk.END)


window = tk.Tk()
window.title("Weather Application")
window.geometry("700x600")

# Create and place the widgets
city_label = tk.Label(window, text="Enter city names separated by commas (e.g., London, Paris, New York):")
city_label.pack(padx=10, pady=10)

city_entry = tk.Entry(window, width=50)
city_entry.pack(padx=10, pady=10)

fetch_button = tk.Button(window, text="Get Weather", command=fetch_weather)
fetch_button.pack(padx=10, pady=10)

# Label for city list
city_list_label = tk.Label(window, text="City List and Weather Information:")
city_list_label.pack(padx=10, pady=5)

# Weather results area
result_text = tk.Text(window, height=15, width=70, wrap=tk.WORD, bd=2, relief=tk.SUNKEN)
result_text.pack(padx=10, pady=10)

# Separator between sections
separator = tk.Label(window, text="--------------------------------------------------")
separator.pack(pady=5)

# Label for statistics
statistics_label = tk.Label(window, text="Statistics:")
statistics_label.pack(padx=10, pady=5)

# Statistics display (Black background)
stats_text = tk.Text(window, height=6, width=70, wrap=tk.WORD, bd=2, relief=tk.SUNKEN, bg="black", fg="white")
stats_text.pack(padx=10, pady=10)

window.mainloop()