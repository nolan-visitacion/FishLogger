import psycopg2
import os

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'testdb'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        self.cur = self.conn.cursor()

    #insert into database
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def insert_user(self, name):
        sql_insert = 'INSERT INTO "users" (name) VALUES (%s) RETURNING user_id;'
        self.cur.execute(sql_insert, (name,))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def insert_lure(self, maker, material, description):
        sql_insert = 'INSERT INTO lure (maker, material, description) VALUES (%s, %s, %s) RETURNING lure_id;'
        self.cur.execute(sql_insert, (maker, material, description))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def insert_location(self, description, city, state_id, body_of_water):
        sql_insert = 'INSERT INTO location (description, city, state_id, body_of_water) VALUES (%s, %s, %s, %s) RETURNING location_id;'
        self.cur.execute(sql_insert, (description, city, state_id, body_of_water))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def insert_fish(self, name, subspecies, color):
        sql_insert = 'INSERT INTO fish (name, subspecies, color) VALUES (%s, %s, %s) RETURNING fish_id;'
        self.cur.execute(sql_insert, (name, subspecies, color))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def insert_weather(self, forecast_date, location_id, temperature, condition):
        sql_insert = '''
        INSERT INTO weather (forecast_date, location_id, temperature, condition)
        VALUES (%s, %s, %s, %s) RETURNING weather_id;
        '''
        self.cur.execute(sql_insert, (forecast_date, location_id, temperature, condition))
        self.conn.commit()
        return self.cur.fetchone()[0]

    def insert_catch(self, fish_id, user_id, lure_id, weather_id, weight, length):
        sql_insert = """
        INSERT INTO Catch (fish_id, user_id, lure_id, weather_id, weight, length)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING catch_id;
        """
        self.cur.execute(sql_insert, (fish_id, user_id, lure_id, weather_id, weight, length))
        self.conn.commit()
        return self.cur.fetchone()[0]
    
    #get info by id
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def query_user_info(self, user_id):

        self.cur.execute('SELECT name FROM users WHERE user_id = %s', (user_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def query_lure_info(self, lure_id):

        self.cur.execute('SELECT maker, material, description FROM lure WHERE lure_id = %s', (lure_id,))
        result = self.cur.fetchone()
        return result if result else None

    def query_location_info(self, location_id):

        self.cur.execute('''
            SELECT l.description, l.city, s.name, l.body_of_water 
            FROM location l
            JOIN state s ON l.state_id = s.state_id
            WHERE location_id = %s
        ''', (location_id,))
        result = self.cur.fetchone()
        return result if result else None

    def query_fish_info(self, fish_id):
        self.cur.execute('SELECT name, subspecies, color FROM fish WHERE fish_id = %s', (fish_id,))
        result = self.cur.fetchone()
        return result if result else None

    def query_weather_info(self, weather_id):

        self.cur.execute('SELECT forecast_date, temperature, condition FROM weather WHERE weather_id = %s', (weather_id,))
        result = self.cur.fetchone()
        return result if result else None

    def query_catch_info(self, catch_id):

        self.cur.execute('''
            SELECT c.fish_id, c.user_id, c.lure_id, c.weather_id, c.weight, c.length
            FROM catch c
            WHERE c.catch_id = %s
        ''', (catch_id,))
        result = self.cur.fetchone()
        return result if result else None
    
    def query_all_catches_by_user(self, user_id):

        self.cur.execute('''
            SELECT c.catch_id, c.fish_id, c.user_id, c.lure_id, c.weather_id, w.location_id, c.weight, c.length
            FROM catch c
            JOIN weather w ON c.weather_id = w.weather_id
            WHERE c.user_id = %s;
        ''', (user_id,))
        result = self.cur.fetchall()
        
        catches = []
        for row in result:
            catch = {
                'catch_id': row[0],
                'fish_id': row[1],
                'user_id': row[2],
                'lure_id': row[3],
                'weather_id': row[4],
                'location_id': row[5],
                'weight': row[6],
                'length': row[7],
            }
            catches.append(catch)
        
        return catches

    #getting ids by name
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_user_id(self, username):
            self.cur.execute('SELECT user_id FROM users WHERE name = %s', (username,))
            result = self.cur.fetchone()
            return result[0] if result else None

    def get_state_id(self, state_name):
        self.cur.execute('SELECT state_id FROM state WHERE name = %s;', (state_name,))
        result = self.cur.fetchone()
        return result[0] if result else None
    
    def get_location_id(self, city, state):
        state_id = self.get_state_id(state)
        sql_query = 'SELECT location_id FROM location WHERE city = %s AND state_id = %s;'
        self.cur.execute(sql_query, (city, state_id))
        result = self.cur.fetchone()
        return result[0] if result else None
   
    #weather related queries
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    """
    def weather_data_exists(self, location_id, forecast_date):
        try:
            weather_id = self.get_weather_by_date_location(forecast_date, location_id)
            return weather_id is not None
        except Exception as e:
            print(f"Error checking weather data: {e}")
            return False
    
    def get_weather_by_date_location(self, forecast_date, location_id):
        sql_query = '''
        SELECT weather_id FROM weather
        WHERE forecast_date = %s AND location_id = %s;
        '''
        self.cur.execute(sql_query, (forecast_date, location_id))
        result = self.cur.fetchone()
        return result[0] if result else None
    """
        
    def close_connection(self):
        self.cur.close()
        self.conn.close()