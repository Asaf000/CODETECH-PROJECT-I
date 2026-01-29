"""
Database Configuration and Connection Handler
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
    
    def get_connection(self):
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def initialize_database(self):
        """Initialize database and create tables"""
        try:
            # Connect without database first
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Create weather_data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    city VARCHAR(100),
                    temperature FLOAT,
                    description VARCHAR(255),
                    humidity INT,
                    wind_speed FLOAT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create news_data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS news_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(500),
                    description TEXT,
                    url TEXT,
                    source VARCHAR(255),
                    published_at DATETIME,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create search_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    search_type VARCHAR(50),
                    search_query VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            connection.commit()
            print("Database and tables created successfully!")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:
            print(f"Error initializing database: {e}")
            return False

def insert_weather_data(city, temperature, description, humidity, wind_speed):
    """Insert weather data into database"""
    db_config = DatabaseConfig()
    connection = db_config.get_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO weather_data (city, temperature, description, humidity, wind_speed)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (city, temperature, description, humidity, wind_speed))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error inserting weather data: {e}")
            return False
    return False

def insert_news_data(articles):
    """Insert news articles into database"""
    db_config = DatabaseConfig()
    connection = db_config.get_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO news_data (title, description, url, source, published_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            for article in articles:
                cursor.execute(query, (
                    article['title'],
                    article['description'],
                    article['url'],
                    article['source'],
                    article['published_at']
                ))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error inserting news data: {e}")
            return False
    return False

def log_search(search_type, search_query):
    """Log search history"""
    db_config = DatabaseConfig()
    connection = db_config.get_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO search_history (search_type, search_query) VALUES (%s, %s)"
            cursor.execute(query, (search_type, search_query))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error logging search: {e}")
            return False
    return False

def get_recent_searches(limit=10):
    """Get recent search history"""
    db_config = DatabaseConfig()
    connection = db_config.get_connection()
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT search_type, search_query, timestamp 
                FROM search_history 
                ORDER BY timestamp DESC 
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
        except Error as e:
            print(f"Error fetching search history: {e}")
            return []
    return []