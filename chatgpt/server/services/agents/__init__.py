# -*- coding: utf-8 -*-

import requests
import json

def get_weather(city):
    """
    Get weather information for a specific city from a weather API.
    :param city: The name of the city.
    :return: A dictionary containing weather information, or None if an error occurred.
    """
    url = f"http://wthrcdn.etouch.cn/weather_mini?city={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response.encoding = 'utf-8'
        data = json.loads(response.text)

        if data['desc'] == 'OK':
            return data['data']
        else:
            print(f"Error: {data['desc']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None

if __name__ == '__main__':
    city_name = "北京"  # Example city name
    weather_data = get_weather(city_name)

    if weather_data:
        print(f"Weather in {city_name}:")
        print(f"Temperature: {weather_data['wendu']}°C")
        print(f"Air Quality: {weather_data['quality']}")
        print("Forecast:")
        for forecast in weather_data['forecast']:
            print(f"  {forecast['date']}: {forecast['type']}, High: {forecast['high']}, Low: {forecast['low']}")
    else:
        print(f"Could not retrieve weather information for {city_name}")
