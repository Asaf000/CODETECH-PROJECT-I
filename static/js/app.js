// API Integration Dashboard - JavaScript
// Handles dynamic data loading and user interactions

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchWeatherBtn = document.getElementById('searchWeatherBtn');
const weatherLoading = document.getElementById('weatherLoading');
const weatherError = document.getElementById('weatherError');
const weatherData = document.getElementById('weatherData');

const categorySelect = document.getElementById('categorySelect');
const countrySelect = document.getElementById('countrySelect');
const searchNewsBtn = document.getElementById('searchNewsBtn');
const newsLoading = document.getElementById('newsLoading');
const newsError = document.getElementById('newsError');
const newsContainer = document.getElementById('newsContainer');

const refreshHistoryBtn = document.getElementById('refreshHistoryBtn');
const searchHistory = document.getElementById('searchHistory');

// Initialize app on page load
document.addEventListener('DOMContentLoaded', () => {
    // Load default data
    fetchWeather('London');
    fetchNews('general', 'us');
    loadSearchHistory();

    // Event listeners
    searchWeatherBtn.addEventListener('click', () => {
        const city = cityInput.value.trim();
        if (city) {
            fetchWeather(city);
        }
    });

    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const city = cityInput.value.trim();
            if (city) {
                fetchWeather(city);
            }
        }
    });

    searchNewsBtn.addEventListener('click', () => {
        const category = categorySelect.value;
        const country = countrySelect.value;
        fetchNews(category, country);
    });

    refreshHistoryBtn.addEventListener('click', loadSearchHistory);
});

// Fetch Weather Data
async function fetchWeather(city) {
    // Show loading state
    weatherLoading.classList.remove('hidden');
    weatherError.classList.add('hidden');
    weatherData.classList.add('hidden');

    try {
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        const result = await response.json();

        weatherLoading.classList.add('hidden');

        if (result.success) {
            displayWeather(result.data);
            loadSearchHistory(); // Refresh history after successful search
        } else {
            showWeatherError(result.error || 'Failed to fetch weather data');
        }
    } catch (error) {
        weatherLoading.classList.add('hidden');
        showWeatherError('Network error. Please try again.');
        console.error('Weather fetch error:', error);
    }
}

// Display Weather Data
function displayWeather(data) {
    weatherData.classList.remove('hidden');

    // Update weather icon
    const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@4x.png`;
    document.getElementById('weatherIcon').src = iconUrl;
    document.getElementById('weatherIcon').alt = data.description;

    // Update weather info
    document.getElementById('cityName').textContent = `${data.city}, ${data.country}`;
    document.getElementById('temperature').textContent = `${data.temperature}°C`;
    document.getElementById('description').textContent = data.description;

    // Update details
    document.getElementById('feelsLike').textContent = `${data.feels_like}°C`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
    document.getElementById('pressure').textContent = `${data.pressure} hPa`;

    // Update timestamp
    document.getElementById('weatherTimestamp').textContent = `Updated: ${data.timestamp}`;
}

// Show Weather Error
function showWeatherError(message) {
    weatherError.textContent = `⚠️ ${message}`;
    weatherError.classList.remove('hidden');
}

// Fetch News Data
async function fetchNews(category, country) {
    // Show loading state
    newsLoading.classList.remove('hidden');
    newsError.classList.add('hidden');
    newsContainer.innerHTML = '';

    try {
        const response = await fetch(`/api/news?category=${category}&country=${country}`);
        const result = await response.json();

        newsLoading.classList.add('hidden');

        if (result.success) {
            displayNews(result.data);
            loadSearchHistory(); // Refresh history after successful search
        } else {
            showNewsError(result.error || 'Failed to fetch news data');
        }
    } catch (error) {
        newsLoading.classList.add('hidden');
        showNewsError('Network error. Please try again.');
        console.error('News fetch error:', error);
    }
}

// Display News Articles
function displayNews(articles) {
    newsContainer.innerHTML = '';

    if (articles.length === 0) {
        newsContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No articles found.</p>';
        return;
    }

    articles.forEach(article => {
        const articleElement = createNewsArticle(article);
        newsContainer.appendChild(articleElement);
    });
}

// Create News Article Element
function createNewsArticle(article) {
    const articleDiv = document.createElement('div');
    articleDiv.className = 'news-article';

    const imageUrl = article.urlToImage || 'https://via.placeholder.com/400x200?text=No+Image';
    
    const publishDate = new Date(article.publishedAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });

    articleDiv.innerHTML = `
        <img src="${imageUrl}" alt="${article.title}" class="news-image" 
             onerror="this.src='https://via.placeholder.com/400x200?text=No+Image'">
        <div class="news-content">
            <h3 class="news-title">${escapeHtml(article.title)}</h3>
            <p class="news-description">${escapeHtml(article.description)}</p>
            <div class="news-meta">
                <span class="news-source"><i class="fas fa-bookmark"></i> ${escapeHtml(article.source)}</span>
                <span>${publishDate}</span>
            </div>
            <div style="margin-top: 1rem;">
                <a href="${article.url}" target="_blank" class="news-link">
                    Read Full Article <i class="fas fa-external-link-alt"></i>
                </a>
            </div>
        </div>
    `;

    return articleDiv;
}

// Show News Error
function showNewsError(message) {
    newsError.textContent = `⚠️ ${message}`;
    newsError.classList.remove('hidden');
}

// Load Search History
async function loadSearchHistory() {
    try {
        const response = await fetch('/api/search-history');
        const result = await response.json();

        if (result.success) {
            displaySearchHistory(result.data);
        }
    } catch (error) {
        console.error('Error loading search history:', error);
    }
}

// Display Search History
function displaySearchHistory(history) {
    searchHistory.innerHTML = '';

    if (history.length === 0) {
        searchHistory.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No search history yet.</p>';
        return;
    }

    history.forEach(item => {
        const historyElement = createHistoryItem(item);
        searchHistory.appendChild(historyElement);
    });
}

// Create History Item Element
function createHistoryItem(item) {
    const historyDiv = document.createElement('div');
    historyDiv.className = 'history-item';

    const icon = item.search_type === 'weather' 
        ? '<i class="fas fa-cloud-sun"></i>' 
        : '<i class="fas fa-newspaper"></i>';

    const timeAgo = getTimeAgo(new Date(item.timestamp));

    historyDiv.innerHTML = `
        <div class="history-icon">${icon}</div>
        <div class="history-details">
            <div class="history-type">${escapeHtml(item.search_type)}</div>
            <div class="history-query">${escapeHtml(item.search_query)}</div>
            <div class="history-time">${timeAgo}</div>
        </div>
    `;

    return historyDiv;
}

// Utility: Get time ago string
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60,
        second: 1
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
        }
    }
    
    return 'Just now';
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});