import unittest
from unittest.mock import MagicMock, patch, call
from controller import FishingLoggerController
from view import View

class TestView(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock()
        self.view = View(self.controller)

    @patch('builtins.input', side_effect=['Gooba'])
    @patch('builtins.print')
    def test_get_username(self, mock_print, mock_input):
        result = self.view.get_username()
        mock_input.assert_called_once_with("Enter your username:")
        self.assertEqual(result, 'Gooba')
        mock_print.assert_called_once_with("Let's start by getting your username...")

    @patch('builtins.input', side_effect=['Trout', 'Rainbow', 'Silver'])
    @patch('builtins.print')
    def test_get_fish_info(self, mock_print, mock_input):
        fish_name, subspecies, fish_color = self.view.get_fish_info()
        
        self.assertEqual(fish_name, 'Trout')
        self.assertEqual(subspecies, 'Rainbow')
        self.assertEqual(fish_color, 'Silver')
        
        mock_print.assert_called_once_with("Now let's hear about your fish!")
        
        expected_input_calls = [
            unittest.mock.call("Enter the fish name: "),
            unittest.mock.call("Enter the fish subspecies: "),
            unittest.mock.call("Enter the fish color: ")
        ]
        mock_input.assert_has_calls(expected_input_calls)

    @patch('builtins.input', side_effect=['Ocean Park', '1', 'Albany', 'New York'])  
    @patch('builtins.print')
    def test_get_location_info(self, mock_print, mock_input):
        result = self.view.get_location_info()

        self.assertEqual(result, ('Ocean Park', 'Albany', 'New York', 'Ocean'))

        expected_input_calls = [
            call("Enter the location name: "),
            call("Enter the number for the body of water: "),
            call("Enter the city name: "),
            call("Enter the state name: ")
        ]
        mock_input.assert_has_calls(expected_input_calls)

        expected_print_calls = [
            call("Where did you catch your fish?"),
            call("NOTE: # Omit the type of water you caught your fish in #"),
            call("Select a body of water:"),
            call("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"),
            call("1. Ocean"),
            call("2. Sea"),
            call("3. River"),
            call("4. Lake"),
            call("5. Pond"),
            call("6. Stream"),
            call("7. Bay"),
            call("8. Gulf"),
            call("9. Lagoon"),
            call("10. Other"),
            call("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"),
            call("Now, let's figure out the city and state you caught your fish.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=True)

        with patch('builtins.input', side_effect=['Ocean Park', '11', 'Albany', 'New York']):  
            result_invalid = self.view.get_location_info()
            self.assertIsNone(result_invalid, "Should return None for invalid body of water input")

    @patch('builtins.input', side_effect=['2024-12-31', '72', 'Sunny'])
    @patch('builtins.print')
    def test_get_weather_info(self, mock_print, mock_input):
        with patch.object(self.view, 'get_location_info', return_value=('Ocean Park', 'Albany', 'New York', 'Ocean')):
            result = self.view.get_weather_info()

        self.assertEqual(result, ('2024-12-31', 72.0, 'Sunny', 'Ocean Park', 'Albany', 'New York', 'Ocean'))

        expected_input_calls = [
            call("Enter the catch date (YYYY-MM-DD): "),
            call("Enter the temperature (in F): "),
            call("Enter the weather description: ")
        ]
        mock_input.assert_has_calls(expected_input_calls)

        expected_print_calls = [
        ]
        if expected_print_calls:  
            mock_print.assert_has_calls(expected_print_calls, any_order=False)

        if not expected_print_calls:
            mock_print.assert_not_called()

    @patch('builtins.input', side_effect=['Maker', 'Material', 'Description'])
    @patch('builtins.print')
    def test_get_lure_info(self, mock_print, mock_input):
        result = self.view.get_lure_info()
        self.assertEqual(result, ('Maker', 'Material', 'Description'))
        mock_print.assert_called_with('Describe the type of lure...')
    
    @patch('builtins.print')
    def test_print_weather_data_with_data(self, mock_print):
        weather_data = [
            ('2024-12-31', '72', 'Sunny'),
            ('2025-01-01', '65', 'Cloudy')
        ]
        city = 'Albany'
        state = 'New York'

        self.view.print_weather_data(weather_data, city, state)

        expected_calls = [
            call(f"Weather forecast for ALBANY, NEW YORK:\n"),
            call(f"Date: 2024-12-31, Temperature: 72°F, Condition: SUNNY"),
            call(f"Date: 2025-01-01, Temperature: 65°F, Condition: CLOUDY")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.print')
    def test_print_weather_data_no_data(self, mock_print):
        weather_data = []
        city = 'Albany'
        state = 'New York'

        self.view.print_weather_data(weather_data, city, state)

        mock_print.assert_called_once_with(f"No weather data available for ALBANY, NEW YORK.")
    
    @patch('builtins.print')
    def test_display_catch_details_with_data(self, mock_print):
        catch_details = [
            {
                'User': 'GOOBA',
                'Fish': ['Trout', 'Rainbow'],
                'Lure': ['Worm', 'Red', 'Small'],
                'Location': ['Lake Pleasant', 'Peoria', 'Arizona', 'USA'],
                'Weather': ['2024-12-31', '65', 'Cloudy'],
                'Weight': '4',
                'Length': '20'
            }
        ]

        self.view.display_catch_details(catch_details)

        expected_calls = [
            call("Catch Details for User: GOOBA"),
            call("-" * 80),
            call("Catch #1"),
            call("Fish: TROUT - RAINBOW"),
            call("Lure: WORM, RED, SMALL"),
            call("Location: LAKE PLEASANT - PEORIA, ARIZONA, USA"),
            call("Weather on 2024-12-31: Temperature: 65.00°F, Condition: CLOUDY"),
            call("Weight: 4 lbs, Length: 20 inches"),
            call("-" * 80)
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.print')
    def test_display_catch_details_no_data(self, mock_print):
        catch_details = []

        self.view.display_catch_details(catch_details)

        mock_print.assert_called_once_with("No catches found to display.")
    
    @patch('builtins.print')
    def test_get_forecast_search(self, mock_print):
        self.controller.db.get_location_id.return_value = None
        self.controller.db.get_state_id.return_value = 1
        self.controller.db.insert_location.return_value = 1

        self.view.get_forecast_search("Springfield", "Illinois", "Lake Springfield", "Lake")

        self.controller.record_weather_data.assert_called_once_with("Springfield", "Illinois", 1)
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
