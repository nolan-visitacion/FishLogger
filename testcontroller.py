import unittest
from controller import FishingLoggerController
from unittest.mock import patch

class TestController(unittest.TestCase):
    
    #setUp() to create a controller was causing db functions to not be called. 
    #Could not get it to work so solved by creating controller in each function

    @patch('controller.Database')
    def test_add_user_found_in_db(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.get_user_id.return_value = 1
        result = controller.add_user("Gooba")

        mock_db.return_value.get_user_id.assert_called_with("GOOBA")
        mock_db.return_value.insert_user.assert_not_called()

        self.assertEqual(result, 1)

    @patch('controller.Database')
    def test_add_user_not_found_in_db(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.get_user_id.return_value = None
        mock_db.return_value.insert_user.return_value = 2

        result = controller.add_user("Gooba")

        mock_db.return_value.get_user_id.assert_called_with("GOOBA")
        mock_db.return_value.insert_user.assert_called_with("GOOBA")
        self.assertEqual(result, 2)
    
    @patch('controller.Database')
    def test_add_lure(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.insert_lure.return_value = 1
        result = controller.add_lure("Brand", "Plastic", "Worm")
        mock_db.return_value.insert_lure.assert_called_with("BRAND", "PLASTIC", "WORM")
        self.assertEqual(result, 1)
    
    @patch('controller.Database')
    def test_add_location(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.get_state_id.return_value = 1
        mock_db.return_value.insert_location.return_value = 2
        result = controller.add_location("Pier", "Long Beach", "California", "Ocean")
        mock_db.return_value.get_state_id.assert_called_with("CALIFORNIA")
        mock_db.return_value.insert_location.assert_called_with("PIER", "LONG BEACH", 1, "OCEAN")
        self.assertEqual(result, 2)
    
    @patch('controller.Database')
    def test_add_fish(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.insert_fish.return_value = 1
        result = controller.add_fish("Trout", "Rainbow", "Silver")
        mock_db.return_value.insert_fish.assert_called_with("TROUT", "RAINBOW", "SILVER")
        self.assertEqual(result, 1)
    
    @patch('controller.FishingLoggerController.add_location')
    @patch('controller.Database')
    def test_add_weather(self, mock_db, mock_add_location):
        controller = FishingLoggerController()

        mock_add_location.return_value = 1  
        mock_db.return_value.insert_weather.return_value = 2  

        result = controller.add_weather('2024-05-08', 75, 'Clear', 'Central Park', 'New York', 'NY', 'Lake')

        mock_add_location.assert_called_with('CENTRAL PARK', 'NEW YORK', 'NY', 'LAKE')
        mock_db.return_value.insert_weather.assert_called_with('2024-05-08', 1, 75, 'CLEAR')
        self.assertEqual(result, 2)
    
    @patch('controller.Database')
    def test_add_catch(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.insert_catch.return_value = 3  

        result = controller.add_catch(1, 2, 3, 4, 5.5, 20)

        mock_db.return_value.insert_catch.assert_called_with(1, 2, 3, 4, 5.5, 20)
        self.assertEqual(result, 3)
    
    @patch('controller.FishingLoggerController.record_weather_data')
    @patch('controller.Database')
    def test_record_catch(self, mock_db, mock_weather):
        controller = FishingLoggerController()

        mock_db.return_value.get_user_id.return_value = None
        mock_db.return_value.insert_user.return_value = 1
        mock_db.return_value.insert_fish.return_value = 2
        mock_db.return_value.insert_lure.return_value = 3
        mock_db.return_value.get_location_id.return_value = 4
        mock_weather.return_value = 5
        mock_db.return_value.insert_catch.return_value = 6
        
        result = controller.record_catch("Gooba", "Trout", "Rainbow", "Silver", 10, 1.5, "Lake Tahoe", "California", "Kastmaster", "Metal", "Spinner")
        
        mock_db.return_value.insert_user.assert_called_with("GOOBA")
        mock_db.return_value.insert_fish.assert_called_with("TROUT", "RAINBOW", "SILVER")
        mock_db.return_value.insert_lure.assert_called_with("KASTMASTER", "METAL", "SPINNER")
        mock_weather.assert_called_with("Lake Tahoe", "California", 4)
        mock_db.return_value.insert_catch.assert_called_with(2, 1, 3, 5, 1.5, 10)

    @patch('requests.get')
    def test_fetch_weather_data(self, mock_get):
        controller = FishingLoggerController()

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"list": [{"main": {"temp": 70}, "weather": [{"description": "clear"}], "dt_txt": "2024-05-08 12:00:00"}]}
        
        result = controller.fetch_weather_data("Las Vegas", "Nevada")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['main']['temp'], 70)
        mock_get.assert_called_with("http://api.openweathermap.org/data/2.5/forecast", params={'q': 'Las Vegas,Nevada,US', 'appid': controller.weather_api_key, 'units': 'imperial'})


    @patch('controller.Database')
    def test_show_catch_details_for_user_with_catches(self, mock_db):
        controller = FishingLoggerController()

        mock_db.return_value.get_user_id.return_value = 1
        mock_db.return_value.query_all_catches_by_user.return_value = [
            {'fish_id': 1, 'lure_id': 1, 'location_id': 1, 'weather_id': 1, 'weight': 5, 'length': 10}
        ]
        mock_db.return_value.query_fish_info.return_value = 'Trout'
        mock_db.return_value.query_lure_info.return_value = 'Spinner'
        mock_db.return_value.query_location_info.return_value = 'Lake'
        mock_db.return_value.query_weather_info.return_value = 'Sunny'

        result = controller.show_catch_details_for_user("Gooba")

        self.assertEqual(len(result), 1)
        self.assertDictEqual(result[0], {
            "User": "Gooba",
            "Fish": 'Trout',
            "Lure": 'Spinner',
            "Location": 'Lake',
            "Weather": 'Sunny',
            "Weight": 5,
            "Length": 10
        })

    @patch('controller.Database')
    def test_show_catch_details_for_user_no_user(self, mock_db):
        controller = FishingLoggerController()
        
        mock_db.return_value.get_user_id.return_value = None

        result = controller.show_catch_details_for_user("Gooba")

        self.assertEqual(result, [])
        mock_db.return_value.query_all_catches_by_user.assert_not_called()

    @patch('controller.FishingLoggerController.fetch_weather_data')
    @patch('controller.Database')
    def test_record_weather_data_success(self, mock_db, mock_fetch_weather):
        controller = FishingLoggerController()

        mock_fetch_weather.return_value = [
            {'main': {'temp': 72}, 'weather': [{'description': 'Clear'}], 'dt_txt': '2024-05-08 12:00:00'}
        ]
        mock_db.return_value.insert_weather.return_value = 1

        result = controller.record_weather_data("New York", "NY", 1)

        self.assertIsNotNone(result)
        mock_db.return_value.insert_weather.assert_called_with('2024-05-08', 1, 72, 'Clear')

    @patch('controller.FishingLoggerController.fetch_weather_data')
    def test_record_weather_data_failure_no_data(self, mock_fetch_weather):
        controller = FishingLoggerController()

        mock_fetch_weather.return_value = []

        result = controller.record_weather_data("New York", "NY", 1)

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
