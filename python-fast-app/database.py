import mysql.connector
import os
import time

class Database:
    def __init__(self):
        # Wait for MySQL container to start up
        time.sleep(5)  # Adjust the delay as needed

        # Database connection configuration
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

        # Establish a database connection
        self.db_connection = mysql.connector.connect(**self.db_config)
        self.db_cursor = self.db_connection.cursor()

    def search_movies_by_year(self, year_of_release):
        query = "SELECT * FROM hollywood WHERE year_of_release = %s"
        self.db_cursor.execute(query, (year_of_release,))
        results = self.db_cursor.fetchall()

        return results

    def upload_movie_data(self, movie_name, year_of_release, box_office, director, producer, cast):
        query = "INSERT INTO hollywood (movie_name, year_of_release, box_office, director, producer, cast) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (movie_name, year_of_release, box_office, director, producer, cast)
        self.db_cursor.execute(query, values)
        self.db_connection.commit()

    def close_connection(self):
        self.db_cursor.close()
        self.db_connection.close()

# Usage example
if __name__ == "__main__":
    db = Database()
    # Perform operations using db.search_movies_by_year() or db.upload_movie_data()
    db.close_connection()

