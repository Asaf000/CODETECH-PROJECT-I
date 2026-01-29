"""
API Integration Dashboard - Main Application
Fetches and displays Weather and News data from public APIs
"""
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from config.database import (
    DatabaseConfig, insert_weather_data, insert_news_data, 
    log_search, get_recent_searches
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
NEWS_BASE_URL = "https://newsapi.org/v2/top-headlines"

# Initialize database on startup
db_config = DatabaseConfig()
db_config.initialize_database()

@app.route('/')
def index():
    """Render main dashboard page"""
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Fetch weather data from OpenWeatherMap API"""
    city = request.args.get('city', 'London')
    
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'], 1),
                'pressure': data['main']['pressure'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Store in database
            insert_weather_data(
                weather_data['city'],
                weather_data['temperature'],
                weather_data['description'],
                weather_data['humidity'],
                weather_data['wind_speed']
            )
            
            # Log search
            log_search('weather', city)
            
            return jsonify({'success': True, 'data': weather_data})
        else:
            return jsonify({'success': False, 'error': 'City not found'}), 404
            
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """Fetch news data from NewsAPI"""
    category = request.args.get('category', 'general')
    country = request.args.get('country', 'us')
    
    try:
        params = {
            'apiKey': NEWS_API_KEY,
            'category': category,
            'country': country,
            'pageSize': 10
        }
        
        response = requests.get(NEWS_BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            articles = []
            articles_to_store = []
            
            for article in data.get('articles', []):
                if article['title'] and article['title'] != '[Removed]':
                    article_data = {
                        'title': article['title'],
                        'description': article.get('description', 'No description available'),
                        'url': article['url'],
                        'urlToImage': article.get('urlToImage', ''),
                        'source': article['source']['name'],
                        'publishedAt': article['publishedAt'],
                        'author': article.get('author', 'Unknown')
                    }
                    articles.append(article_data)
                    
                    # Prepare for database storage
                    articles_to_store.append({
                        'title': article_data['title'],
                        'description': article_data['description'],
                        'url': article_data['url'],
                        'source': article_data['source'],
                        'published_at': datetime.strptime(
                            article['publishedAt'], 
                            '%Y-%m-%dT%H:%M:%SZ'
                        )
                    })
            
            # Store in database
            if articles_to_store:
                insert_news_data(articles_to_store)
            
            # Log search
            log_search('news', f'{category} - {country}')
            
            return jsonify({'success': True, 'data': articles})
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch news'}), 404
            
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search-history', methods=['GET'])
def search_history():
    """Get recent search history from database"""
    try:
        history = get_recent_searches(15)
        return jsonify({'success': True, 'data': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', True), port=5000)