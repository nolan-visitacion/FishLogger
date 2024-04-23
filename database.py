import psycopg2

class Database:
    
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname = "catch_log",
            user = "postgres",
            password = "password",
            host = 'localhost',
            port = 5432
        )
        self.cur = self.conn.cursor()

    def get_lebron_catch(self):
        sql_query = """
    SELECT
        c.catch_id,
        c.date AS catch_date,
        f.name AS fish_name,
        f.subspecies,
        f.color AS fish_color,
        l.description AS location_description,
        l.body_of_water,
        c.weight,
        c.length,
        lr.description AS lure_description
    FROM 
        Catch c
        JOIN "User" u ON c.user_id = u.user_id
        JOIN Fish f ON c.fish_id = f.fish_id
        JOIN "Location" l ON c.location_id = l.location_id
        JOIN Lure lr ON c.lure_id = lr.lure_id
    WHERE 
        u.name = 'Lebron James';
    """
        
        self.cur.execute(sql_query)
        result = self.cur.fetchall()
        return result
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()

