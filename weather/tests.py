from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch, MagicMock
from weather.services import fetch_weather_data
from weather.views import rate_limit_exceeded_view
from django_ratelimit.exceptions import Ratelimited
import json

class WeatherViewTests(TestCase):
    def setUp(self):
        self.city_name = "Mumbai"
        self.valid_weather_data = {
            "city": "Mumbai",
            "temperature": "15°C",
            "feels_like": "13°C",
            "description": "Clear",
            "humidity": "50%",
            "wind_speed": "10 km/h"
        }
        self.cache_key = f"weather_{self.city_name.lower()}"

    @patch('weather.services.fetch_weather_data')
    def test_valid_city_name_fetch_weather_data(self, mock_fetch_weather_data):
        """Test that a valid city name fetches data successfully."""
        mock_fetch_weather_data.return_value = self.valid_weather_data
        
        response = self.client.get(reverse('weather', args=[self.city_name]))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache miss! Data fetched from API.", response.json()["message"])
        self.assertEqual(response.json()["data"], self.valid_weather_data)
        mock_fetch_weather_data.assert_called_once_with(self.city_name)

    def test_invalid_city_name_returns_400(self):
        """Test that an invalid city name returns a 400 response."""
        response = self.client.get(reverse('weather', args=["12345"]))
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"error": "Invalid city name. Please enter a valid city name."}
        )

    @patch('weather.services.fetch_weather_data')
    def test_fetch_weather_data_failure_returns_500(self, mock_fetch_weather_data):
        """Test that an API failure returns a 500 response."""
        mock_fetch_weather_data.return_value = None
        
        response = self.client.get(reverse('weather', args=[self.city_name]))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {"error": "Unable to fetch weather data. Please try again later."}
        )
        mock_fetch_weather_data.assert_called_once_with(self.city_name)

    @patch('weather.services.fetch_weather_data')
    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_cache_hit_returns_cached_data(self, mock_fetch_weather_data):
        """Test that cached weather data is returned when available."""
        # Set cache data
        from django.core.cache import cache
        cache.set(self.cache_key, self.valid_weather_data, timeout=43200)

        response = self.client.get(reverse('weather', args=[self.city_name]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache hit!", response.json()["message"])
        self.assertEqual(response.json()["data"], self.valid_weather_data)
        mock_fetch_weather_data.assert_not_called()

    @override_settings(RATELIMIT_VIEW='weather.views.rate_limit_exceeded_view')
    def test_rate_limit_exceeded(self):
        """Test that rate-limited requests are handled correctly."""
        with patch('django_ratelimit.decorators.is_ratelimited', return_value=True):
            response = self.client.get(reverse('weather', args=[self.city_name]))
        
        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            response.json(),
            {"error": "Rate limit exceeded. Please try again later."}
        )

    def test_rate_limit_exceeded_view_direct(self):
        """Test the standalone rate_limit_exceeded_view."""
        response = rate_limit_exceeded_view(None)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(
            json.loads(response.content),
            {"error": "Rate limit exceeded. Please try again later."}
        )
