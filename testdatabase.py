import unittest
from database import Database
from unittest.mock import MagicMock, patch

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.cur = MagicMock()
        self.db.conn = MagicMock()

    #test | insert into database
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_insert_user(self):
        self.db.insert_user("Gooba")
        self.db.cur.execute.assert_called_with('INSERT INTO "users" (name) VALUES (%s) RETURNING user_id;', ("Gooba",))
        self.db.conn.commit.assert_called_once()
    
    def test_insert_lure(self):
        self.db.insert_lure("Panther Martin", "Golden", "Spinner")
        self.db.cur.execute.assert_called_with('INSERT INTO lure (maker, material, description) VALUES (%s, %s, %s) RETURNING lure_id;', ("Panther Martin", "Golden", "Spinner",))
        self.db.conn.commit.assert_called_once()
    
    def test_insert_location(self):
        self.db.insert_location("San Rafael", "Reno", 28, "Pond")
        self.db.cur.execute.assert_called_with('INSERT INTO location (description, city, state_id, body_of_water) VALUES (%s, %s, %s, %s) RETURNING location_id;', ("San Rafael", "Reno", 28, "Pond",))
        self.db.conn.commit.assert_called_once()
    
    def test_insert_fish(self):
        self.db.insert_fish("Trout", "Rainbow", "Silver")
        self.db.cur.execute.assert_called_with('INSERT INTO fish (name, subspecies, color) VALUES (%s, %s, %s) RETURNING fish_id;', ("Trout", "Rainbow", "Silver",))
        self.db.conn.commit.assert_called_once()
    
    def test_insert_weather(self):
        self.db.insert_weather("2024-05-06", 1, 78, "Sunny")
        self.db.cur.execute.assert_called_with('''
        INSERT INTO weather (forecast_date, location_id, temperature, condition)
        VALUES (%s, %s, %s, %s) RETURNING weather_id;
        ''', ("2024-05-06", 1, 78, "Sunny",))
        self.db.conn.commit.assert_called_once()

    def test_insert_catch(self):
        self.db.insert_catch(1, 1, 1, 1, 10, 10)
        self.db.cur.execute.assert_called_with("""
        INSERT INTO Catch (fish_id, user_id, lure_id, weather_id, weight, length)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING catch_id;
        """, (1, 1, 1, 1, 10, 10,))
        self.db.conn.commit.assert_called_once()
    

    #test | get info by id
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_query_user_info(self):
        self.db.cur.fetchone.return_value = ("Gooba",)
        self.db.query_user_info(1)
        self.db.cur.execute.assert_called_with('SELECT name FROM users WHERE user_id = %s', (1,))
        self.assertEqual(self.db.query_user_info(1), "Gooba")
    
    def test_query_lure_info(self):
        self.db.cur.fetchone.return_value = ("Panther Martin", "Golden", "Spinner",)
        self.db.query_lure_info(1)
        self.db.cur.execute.assert_called_with('SELECT maker, material, description FROM lure WHERE lure_id = %s', (1,))
        self.assertEqual(self.db.query_lure_info(1), ("Panther Martin", "Golden", "Spinner"))
    
    def test_query_location_info(self):
        self.db.cur.fetchone.return_value = ("San Rafael", "Reno", 28, "Pond",)
        self.db.query_location_info(1)
        self.db.cur.execute.assert_called_with('''
            SELECT l.description, l.city, s.name, l.body_of_water 
            FROM location l
            JOIN state s ON l.state_id = s.state_id
            WHERE location_id = %s
        ''', (1,))
        self.assertEqual(self.db.query_location_info(1), ("San Rafael", "Reno", 28, "Pond"))

    def test_query_fish_info(self):
        self.db.cur.fetchone.return_value = ("Trout", "Rainbow", "Silver",)
        self.db.query_fish_info(1)
        self.db.cur.execute.assert_called_with('SELECT name, subspecies, color FROM fish WHERE fish_id = %s', (1,))
        self.assertEqual(self.db.query_fish_info(1), ("Trout", "Rainbow", "Silver"))
    
    def test_query_weather_info(self):
        self.db.cur.fetchone.return_value = ("2024-05-06", 1, 78, "Sunny",)
        self.db.query_weather_info(1)
        self.db.cur.execute.assert_called_with('SELECT forecast_date, temperature, condition FROM weather WHERE weather_id = %s', (1,))
        self.assertEqual(self.db.query_weather_info(1), ("2024-05-06", 1, 78, "Sunny"))

    def test_query_catch_info(self):
        self.db.cur.fetchone.return_value = (1, 1, 1, 1, 10, 10)
        self.db.query_catch_info(1)
        self.db.cur.execute.assert_called_with('''
            SELECT c.fish_id, c.user_id, c.lure_id, c.weather_id, c.weight, c.length
            FROM catch c
            WHERE c.catch_id = %s
        ''', (1,))
        self.assertEqual(self.db.query_catch_info(1), (1, 1, 1, 1, 10, 10))

    def test_query_all_catches_by_user(self):
        self.db.cur.fetchall.return_value = [
            (1, 2, 3, 4, 5, 6, 7.5, 20),  
            (2, 3, 3, 5, 6, 7, 8.0, 25)
        ]

        result = self.db.query_all_catches_by_user(1)

        self.db.cur.execute.assert_called_once_with('''
            SELECT c.catch_id, c.fish_id, c.user_id, c.lure_id, c.weather_id, w.location_id, c.weight, c.length
            FROM catch c
            JOIN weather w ON c.weather_id = w.weather_id
            WHERE c.user_id = %s;
        ''', (1,))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['catch_id'], 1)
        self.assertEqual(result[0]['weight'], 7.5)
        self.assertEqual(result[1]['length'], 25)

        self.assertDictEqual(result[0], {
            'catch_id': 1,
            'fish_id': 2,
            'user_id': 3,
            'lure_id': 4,
            'weather_id': 5,
            'location_id': 6,
            'weight': 7.5,
            'length': 20
        })

    #test | getting ids by name
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_get_user_id(self):
        self.db.cur.fetchone.return_value = (1,)
        self.db.get_user_id("Gooba")
        self.db.cur.execute.assert_called_with('SELECT user_id FROM users WHERE name = %s', ("Gooba",))
        self.assertEqual(self.db.get_user_id("Gooba"), (1))
    
    def test_get_state_id(self):
        self.db.cur.fetchone.return_value = (1,)
        self.db.get_state_id("ALABAMA")
        self.db.cur.execute.assert_called_with('SELECT state_id FROM state WHERE name = %s;', ("ALABAMA",))
        self.assertEqual(self.db.get_state_id("ALABAMA"), (1))
    
    @patch('database.Database.get_state_id')  
    def test_get_location_id(self, mock_get_state_id):
        mock_get_state_id.return_value = 1        
        self.db.cur.fetchone.return_value = (1,)
        
        result = self.db.get_location_id("Las Vegas", "Nevada")        
        self.db.cur.execute.assert_called_with(
            'SELECT location_id FROM location WHERE city = %s AND state_id = %s;', 
            ("Las Vegas", 1)  
        )
        self.assertEqual(result, 1)  
        mock_get_state_id.assert_called_once_with("Nevada")


if __name__ == '__main__':
    unittest.main()
