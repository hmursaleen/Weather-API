# 🌦️ **Weather API Project**

A Django-based weather API application that retrieves real-time weather data for cities using a third-party API. This project incorporates **caching**, **rate-limiting**, and adheres to clean coding principles such as **SOLID** and **DRY**.

---

## 🚀 **Features**

- **Real-time Weather Data**: Retrieves temperature, humidity, wind speed, and more for any valid city.
- **Rate Limiting**: Restricts requests to 5 per minute per IP using `django-ratelimit`.
- **Caching with Redis**: Reduces redundant API calls by caching responses for 12 hours.
- **Error Handling**: Handles invalid city names, rate-limit exceedance, and API errors gracefully.
- **Unit Testing**: Comprehensive test coverage for all features.
- **Environment Variable Management**: Secures sensitive data like API keys using `.env`.

---

## 🛠️ **Tech Stack**

- **Backend Framework**: Django
- **Caching**: Redis
- **Key Libraries**:
  - `django-redis` (Redis caching)
  - `django-ratelimit` (Rate-limiting)
  - `python-decouple` (Environment variable management)
  - `requests` (HTTP requests for the third-party API)
- **Testing**: Django's Test Framework with `unittest.mock`

---

## ⚙️ **Prerequisites**

- **Python**: Version 3.8 or higher
- **Redis**: Installed locally or via Docker

---

## 📥 **Installation**

### 1. Clone the Repository
```bash
git clone https://github.com/hmursaleen/Weather-API.git
cd weather-api
```

---


### 2. Create a Virtual Environment
```bash
python -m venv environment_name
source environment_name/bin/activate  # On Windows: environment_name\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory with the following:

```env
# Third-party API configuration
WEATHER_API_KEY=EJ4WZDBWQ2ULF9N85BY5SYWXM
WEATHER_API_BASE_URL=https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline

# Redis configuration
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
```


### 5. Start Redis
If Redis is installed locally:
```bash
redis-server
```
If Redis is running via Docker:

```bash
docker run -d --name redis -p 6379:6379 redis
```

### 6. Run the Django Server
```bash
python manage.py runserver
```

---

## 🧪 **Running Tests**
Run all test cases with:
```bash
python manage.py test
```
---

## 📋 **Usage**
- **Accessing the API**:
Make a GET request to:
```bash
http://localhost:8000/api/weather/<city_name>/
```

Replace <city_name> with the name of the city you want to query.

- **Rate Limit**
If the rate limit (5 requests/minute per IP) is exceeded, the API returns:
```json
{"error": "Rate limit exceeded. Please try again later."}
```

- **Caching**

A cache hit returns:
```json
{"message": "Cache hit!", "data": {...}}
```

A cache miss fetches data from the third-party API:
```json
{"message": "Cache miss! Data fetched from API.", "data": {...}}
```
---

## 📂 **Project Structure**
```bash

weather-api/
├── weather/
│   ├── views.py          # Handles API requests
│   ├── services.py       # Fetches weather data from the third-party API
│   ├── tests.py          # Unit test cases
│   ├── utils.py          # Utility functions for caching
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not committed)
├── README.md             # Project documentation
```
---

## 🧑‍💻 **Contributing**
Contributions are welcome! Please follow these steps:

- **Fork the repository**:
Create a new branch:
```bash
 git checkout -b feature/YourFeature
```

- **Commit your changes**:
```bash
 git commit -m "Add YourFeature"
```

- **Push to the branch**:
```bash
 git push origin feature/YourFeature
```

- **Open a Pull Request**

---

## 📜 **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

## 📧 **Contact**
For inquiries or feedback, contact:

- **Name: Habibul Mursaleen**
- **Email: habibulmursaleen@gmail.com**
- **GitHub: hmursaleen**

---

## 🌟 **Acknowledgments**
- **Django Framework: For providing a robust web development platform.**
- **Redis: For enabling high-performance caching.**
- **Visual Crossing’s API: For offering reliable weather data services.**