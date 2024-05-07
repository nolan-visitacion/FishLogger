import sys

class View:

    def __init__(self, controller):
        self.controller = controller

    def get_user_input(self, prompt):
        return input(prompt).strip()

    def display_menu(self):
        print("\nFishing Logger CLI")
        print("1. Record a Catch")
        print("2. Get Catch Info For A User")
        print("3. Exit")
        return self.get_user_input("Select an option: ")

    # Functions for getting user input
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_username(self):
        print("Let's start by getting your username...")
        return self.get_user_input("Enter your username:")

    def get_fish_info(self):
        print("Now let's hear about your fish!")
        fish_name = self.get_user_input("Enter the fish name: ")
        subspecies = self.get_user_input("Enter the fish subspecies: ")
        fish_color = self.get_user_input("Enter the fish color: ")
        return fish_name, subspecies, fish_color

    def get_length(self):
        print("How long was your fish?")
        return float(self.get_user_input("Enter the fish length (in in): "))

    def get_weight(self):
        print("How much did your fish weigh?")
        return float(self.get_user_input("Enter the fish weight (in lbs): "))

    def get_location_info(self):
        water_body_types = {1: "Ocean", 2: "Sea", 3: "River", 4: "Lake", 5: "Pond", 6: "Stream", 7: "Bay", 8: "Gulf", 9: "Lagoon", 10: "Other"}
        
        print("Where did you catch your fish?")
        print("NOTE: # Omit the type of water you caught your fish in #")
        location_name = self.get_user_input("Enter the location name: ")
        print("Select a body of water:")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for number, description in water_body_types.items():
            print(f"{number}. {description.capitalize()}")   
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        while True:
            try:
                choice = int(input("Enter the number corresponding to body of water: "))
                if choice in water_body_types:
                    body_of_water = water_body_types[choice]
                else:
                    print("Invalid selection. Please select a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            
            print("Now, let's figure out the city and state you caught your fish.")
            city = self.get_user_input("Enter the city name: ")
            state_name = self.get_user_input("Enter the state name: ")

            return location_name, city, state_name, body_of_water
        
    def get_weather_info(self):
        location_name, city, state_name, body_of_water = self.get_location_info(location_name, city, state_name, body_of_water)
        forecast_date = self.get_user_input("Enter the catch date (YYYY-MM-DD): ")
        temperature = float(self.get_user_input("Enter the temperature (in F): "))
        condition = self.get_user_input("Enter the weather description: ")
        return forecast_date, temperature, condition, location_name, city, state_name, body_of_water

    def get_lure_info(self):
        print("Great! Now, let's enter what caught your fish!\n")
        
        print("Name the maker of your lure...")
        maker = self.get_user_input("Enter the lure maker: ")
        print("What is your lure made of?")
        material = self.get_user_input("Enter the lure material: ")
        print("Describe the type of lure...")
        description = self.get_user_input("Enter the lure description: ")
        return maker, material, description

    # displaying info 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def print_weather_data(self, weather_data, city, state):
        if weather_data:
            print(f"Weather forecast for {city.upper()}, {state.upper()}:\n")
            for forecast_date, temperature, condition in weather_data:
                print(f"Date: {forecast_date}, Temperature: {temperature}°F, Condition: {condition.upper()}")
        else:
            print(f"No weather data available for {city.upper()}, {state.upper()}.")

    def display_catch_details(self, catch_details):
        if not catch_details:
            print("No catches found to display.")
            return

        print(f"Catch Details for User: {catch_details[0]['User'].upper()}")
        print("-" * 80) 

        for index, catch in enumerate(catch_details, start=1):
            print(f"Catch #{index}")
            print(f"Fish: {catch['Fish'][0].upper()} - {catch['Fish'][1].upper()}")
            print(f"Lure: {catch['Lure'][0].upper()}, {catch['Lure'][1].upper()}, {catch['Lure'][2].upper()}")
            print(f"Location: {catch['Location'][0].upper()} - {catch['Location'][1].upper()}, {catch['Location'][2].upper()}, {catch['Location'][3].upper()}")
            temperature = float(catch['Weather'][1])
            print(f"Weather on {catch['Weather'][0]}: Temperature: {temperature:.2f}°F, Condition: {catch['Weather'][2].upper()}")
            print(f"Weight: {catch['Weight']} lbs, Length: {catch['Length']} inches")
            print("-" * 80)
    
    #Functions for API
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_forecast_search(self, city, state, location_name, body_of_water):

        city_upper = city.strip().upper()
        state_upper = state.strip().upper()
        location_id = self.controller.db.get_location_id(city_upper, state_upper)

        if location_id is None:
            print(f"{city_upper}, {state_upper} not found in database. Let's add it!")
            state_id = self.controller.db.get_state_id(state_upper)
            location_id = self.controller.db.insert_location(location_name.strip().upper(), city_upper, state_id, body_of_water.strip().upper())

        self.controller.record_weather_data(city, state, location_id)
            

