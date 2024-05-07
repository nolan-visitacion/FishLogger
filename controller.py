from database import Database
from view import View
import requests
import statistics
from collections import Counter
from datetime import datetime, timedelta, time



class FishingLoggerController:
    def __init__(self):
        self.db = Database()
        self.weather_api_key = "0d01eaba5c4a1bb0f3533bd0d6fe3272"


    #add to database
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add_user(self, username):
        if self.db.get_user_id(username.strip().upper()):
            print('found in db')
            return self.db.get_user_id(username.strip().upper()) 
        else:
            return self.db.insert_user(username.strip().upper())

    def add_lure(self, maker, material, description):
        return self.db.insert_lure(maker.strip().upper(), material.strip().upper(), description.strip().upper())

    def add_location(self, description, city, state_name, body_of_water):
        return self.db.insert_location(description.strip().upper(), city.strip().upper(), self.db.get_state_id(state_name.strip().upper()), body_of_water.strip().upper())

    def add_fish(self, fish_name, fish_color):
        return self.db.insert_fish(fish_name.strip().upper(), fish_color.strip().upper())

    def add_weather(self, forecast_date, temperature, condition, location_name, city, state, body_of_water):
        location_id = self.add_location(location_name.strip().upper(), city.strip().upper(), state.strip().upper(), body_of_water.strip().upper())
        return self.db.insert_weather(forecast_date, location_id, temperature, condition.strip().upper())

    def add_catch(self, fish_id, user_id, lure_id, weather_id, weight, length):
        return self.db.insert_catch(fish_id, user_id, lure_id, weather_id, weight, length)

    def record_catch(self, username, fish_name, subspecies, fish_color, length, weight, city, state, maker, material, description):
        user_id = self.add_user(username)
        fish_id = self.db.insert_fish(fish_name.strip().upper(), subspecies.strip().upper(), fish_color.strip().upper())
        lure_id = self.db.insert_lure(maker.strip().upper(), material.strip().upper(), description.strip().upper())
        location_id = self.db.get_location_id(city.strip().upper(), state.strip().upper())
        
        weather_id = self.record_weather_data(city, state, location_id)

        catch_id = self.db.insert_catch(fish_id, user_id, lure_id, weather_id, weight, length)

        print(f"Recorded new catch with id: {catch_id}")
    
    #query from database
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def show_catch_details_for_user(self, username):
        user_id = self.db.get_user_id(username.strip().upper())
        if not user_id:
            print("User not found.")
            return []

        catches = self.db.query_all_catches_by_user(user_id)
        if not catches:
            print("No catches found for this user.")
            return []

        catch_details = []
        for catch in catches:
            # Assuming catch is a tuple or dict with appropriate keys
            fish_info = self.db.query_fish_info(catch['fish_id'])
            lure_info = self.db.query_lure_info(catch['lure_id'])
            location_info = self.db.query_location_info(catch['location_id'])
            weather_info = self.db.query_weather_info(catch['weather_id'])

            # Aggregate all info into a dictionary
            details = {
                "User": username,
                "Fish": fish_info,
                "Lure": lure_info,
                "Location": location_info,
                "Weather": weather_info,
                "Weight": catch['weight'],
                "Length": catch['length']
            }
            catch_details.append(details)

        return catch_details

    #API
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def fetch_weather_data(self, city, state):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': f"{city},{state},US",
            'appid': self.weather_api_key,
            'units': 'imperial'
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            weather_list = response.json().get('list', [])
            return weather_list  
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return []
        
    def record_weather_data(self, city, state, location_id):

        weather_data = self.fetch_weather_data(city, state)
        if not weather_data:
            print("No weather data available to process.")
            return None

        temperatures = [entry['main']['temp'] for entry in weather_data]
        conditions = [entry['weather'][0]['description'] for entry in weather_data]
        mean_temperature = round(statistics.mean(temperatures), 2)
        most_common_condition = Counter(conditions).most_common(1)[0][0]
        forecast_date = weather_data[0]['dt_txt'].split(" ")[0]  # Assuming all entries are from the same date
        

        try:
            weather_id = self.db.insert_weather(forecast_date, location_id, mean_temperature, most_common_condition)
            return weather_id
        except Exception as e:
            print(f"Failed to insert aggregated weather data: {e}")
            return None


