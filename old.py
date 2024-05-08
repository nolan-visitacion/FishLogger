import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="catch_log",
            user="postgres",
            password="password",
            host='localhost',
            port=5432
        )
        self.cur = self.conn.cursor()

    #insert into database
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def insert_user(self, name):
        sql_insert = 'INSERT INTO "user" (name) VALUES (%s) RETURNING user_id;'
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

    def insert_catch(self, fish_id, user_id, date_id, lure_id, weight, length):
        sql_insert = """
        INSERT INTO Catch (fish_id, user_id, date_id, lure_id, weight, length)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING catch_id;
        """
        self.cur.execute(sql_insert, (fish_id, user_id, date_id, lure_id, weight, length))
        self.conn.commit()
        return self.cur.fetchone()[0]
    
    #query database
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_state_id(self, state_name):
        self.cur.execute('SELECT state_id FROM state WHERE name = %s;', (state_name,))
        result = self.cur.fetchone()
        return result[0] if result else None
    
    def get_location_by_city(self, city):
        sql_query = 'SELECT location_id FROM location WHERE city = %s;'
        self.cur.execute(sql_query, (city,))
        result = self.cur.fetchone()
        return result[0] if result else None
    
    def get_weather_by_date_location(self, forecast_date, location_id):
        sql_query = '''
        SELECT weather_id FROM weather
        WHERE forecast_date = %s AND location_id = %s;
        '''
        self.cur.execute(sql_query, (forecast_date, location_id))
        result = self.cur.fetchone()
        return result[0] if result else None
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()