import click
from controller import FishingLoggerController
from view import View

@click.command()
def main():
    controller = FishingLoggerController()
    view = View(controller)

    while True:
        choice = view.display_menu()
        
        if choice == '1':
            username = view.get_username()
            fish_name, subspecies, fish_color = view.get_fish_info()
            length = view.get_length()
            weight = view.get_weight()
            location_name, city, state, body_of_water = view.get_location_info()
            view.get_forecast_search(city, state, location_name, body_of_water)
            # catch_date, temperature, weather_description = view.get_weather_info()
            maker, material, description = view.get_lure_info()

            controller.record_catch(
                username=username,
                fish_name=fish_name,
                subspecies=subspecies,
                fish_color=fish_color,
                length=length,
                weight=weight,
                city=city,
                state=state,
                maker=maker,
                material=material,
                description=description
            )
            print("\nCatch recorded successfully.")
        
        elif choice == '2':
            
            user = input('Enter user for lookup: ')
            catch_details = controller.show_catch_details_for_user(user)
            view.display_catch_details(catch_details)

        elif choice == '3':
            print("Exiting...")
            break
            
if __name__ == "__main__":
    main()
