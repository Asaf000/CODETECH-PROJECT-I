# API Integration Dashboard - Weather & News

## 🌟 Project Overview

A responsive web application that fetches and displays real-time data from public APIs (Weather and News). Built for CODTECH Internship.

**Features:**
- ☁️ Real-time weather information from OpenWeatherMap API
- 📰 Latest news from NewsAPI with category and country filters
- 💾 MySQL database integration for data persistence
- 📊 Search history tracking
- 📱 Fully responsive design for all devices
- 🎨 Modern, dark-themed UI with smooth animations

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **APIs:** OpenWeatherMap API, NewsAPI
- **Configuration:** .env for environment variables

## 📁 Project Structure

```
api_integration_project/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (DO NOT COMMIT)
├── config/
│   └── database.py            # Database configuration & functions
├── templates/
│   └── index.html             # Main HTML template
└── static/
    ├── css/
    │   └── style.css          # Responsive CSS styles
    └── js/
        └── app.js             # JavaScript for dynamic content
```

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.8+** installed
2. **MySQL Server** installed and running
3. **API Keys** (free registration required):
   - [OpenWeatherMap API](https://openweathermap.org/api) - for weather data
   - [NewsAPI](https://newsapi.org/) - for news articles

### Step 1: Clone/Download the Project

```bash
cd api_integration_project
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure MySQL Database

1. Start MySQL server
2. Create a MySQL user (or use root)
3. The application will automatically create the database and tables

### Step 4: Configure Environment Variables

Edit the `.env` file with your credentials:

```env
# API Keys (REQUIRED - Get from respective websites)
WEATHER_API_KEY=your_openweathermap_api_key_here
NEWS_API_KEY=your_newsapi_key_here

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=api_dashboard_db

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

**Important:** 
- Replace `your_openweathermap_api_key_here` with your actual API key from OpenWeatherMap
- Replace `your_newsapi_key_here` with your actual API key from NewsAPI
- Replace `your_mysql_password_here` with your MySQL password

### Step 5: Run the Application

```bash
python app.py
```

The application will:
1. Create the database if it doesn't exist
2. Create necessary tables (weather_data, news_data, search_history)
3. Start the Flask development server

### Step 6: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 How to Use

### Weather Section
1. Enter a city name in the search box
2. Click "Get Weather" to fetch current weather data
3. View temperature, humidity, wind speed, and more

### News Section
1. Select a news category (General, Business, Technology, etc.)
2. Select a country (US, UK, India, Canada, Australia)
3. Click "Get News" to fetch latest articles
4. Click on article links to read full stories

### Search History
- Automatically tracks all weather and news searches
- Shows timestamp of each search
- Click "Refresh" to update the list

## 🗄️ Database Schema

### Tables Created Automatically:

**1. weather_data**
- id (Primary Key)
- city
- temperature
- description
- humidity
- wind_speed
- timestamp

**2. news_data**
- id (Primary Key)
- title
- description
- url
- source
- published_at
- timestamp

**3. search_history**
- id (Primary Key)
- search_type (weather/news)
- search_query
- timestamp

## 🔑 Getting Free API Keys

### OpenWeatherMap API:
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key
5. Paste it in the `.env` file

### NewsAPI:
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Sign up for a free account
4. Copy your API key
5. Paste it in the `.env` file

**Note:** Free tier limitations:
- OpenWeatherMap: 1000 calls/day
- NewsAPI: 100 requests/day

## 🎨 Features Implemented

✅ **API Integration**
- Weather data from OpenWeatherMap
- News articles from NewsAPI
- Error handling for failed requests

✅ **Database Integration**
- MySQL connection management
- Automatic schema creation
- Data persistence
- Search history tracking

✅ **Responsive Design**
- Mobile-first approach
- Tablet and desktop optimized
- Modern gradient backgrounds
- Smooth animations and transitions

✅ **User Experience**
- Real-time data loading
- Loading indicators
- Error messages
- Search history
- External link handling

## 🔒 Security Best Practices

- ✅ Environment variables for sensitive data
- ✅ SQL injection prevention with parameterized queries
- ✅ XSS prevention with HTML escaping
- ✅ HTTPS API calls
- ❗ Never commit `.env` file to version control

## 🐛 Troubleshooting

### Database Connection Error
- Check if MySQL server is running
- Verify database credentials in `.env`
- Ensure MySQL user has CREATE DATABASE permissions

### API Errors
- Verify API keys are correct in `.env`
- Check if you've exceeded free tier limits
- Ensure internet connection is active

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`

## 📝 CODTECH Internship Project

**Deliverable:** ✅ A responsive webpage with API data dynamically loaded and displayed

**Technologies Used:**
- Python (Backend)
- HTML/CSS (Frontend)
- MySQL (Database)
- JavaScript (Dynamic Content)
- Flask (Web Framework)
- REST APIs (Data Integration)

## 📄 License

This project is created for educational purposes as part of CODTECH Internship program.

## 👨‍💻 Author

CODTECH Internship Project - API Integration Dashboard

---

**Note:** Remember to get your completion certificate upon internship end date! 🎓