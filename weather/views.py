'''
key='ip': Limits requests based on the client’s IP address.
rate='5/m': Allows a maximum of 5 requests per minute.
'''

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .services import fetch_weather_data
from .utils import get_from_cache, set_in_cache


'''
The @method_decorator is used to apply the ratelimit decorator to the dispatch method, which ensures that 
all HTTP methods (e.g., GET, POST) are subject to the rate limit.
'''

@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
class WeatherView(View):
    
    def get(self, request, city_name):
        # Validate the city name
        if not city_name or not city_name.isalpha():
            return JsonResponse(
                {"error": "Invalid city name. Please enter a valid city name."},
                status=400
            )

        # Check for cached weather data
        cache_key = f"weather_{city_name.lower()}"
        cached_data = get_from_cache(cache_key)
        if cached_data:
            return JsonResponse({"message": "Cache hit!", "data": cached_data})

        # Fetch weather data from the third-party API
        weather_data = fetch_weather_data(city_name)
        if not weather_data or weather_data is None:
            return JsonResponse(
                {"error": "Unable to fetch weather data. Please try again later."},
                status=500
            )

        # Cache the new data with a 12-hour expiration
        set_in_cache(cache_key, weather_data, expiration=43200)
        return JsonResponse({"message": "Cache miss! Data fetched from API.", "data": weather_data})








def rate_limit_exceeded_view(request, *args):
    """
    Custom view for handling rate-limited requests.
    """
    return JsonResponse(
        {"error": "Rate limit exceeded. Please try again later."},
        status=429
    )