# map_service.py - FINAL VERSION FOR BACKEND

import requests
from geopy.geocoders import Nominatim

def find_hospitals_osm(postal_code, radius=4500):
    """Find nearby hospitals using OpenStreetMap Overpass API based on Indian postal code"""
    # Convert postal code to coordinates (restricted to India)
    try:
        geolocator = Nominatim(user_agent="hospital_finder_app") # Use a descriptive user_agent
        location = geolocator.geocode(f"{postal_code}, India", timeout=10) # Add a timeout

        if not location:
            return f"Invalid postal code: {postal_code}. Please enter a valid Indian pincode."

        latitude, longitude = location.latitude, location.longitude

        # Overpass API query for hospitals
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        (
          node["amenity"="hospital"](around:{radius},{latitude},{longitude});
          way["amenity"="hospital"](around:{radius},{latitude},{longitude});
          relation["amenity"="hospital"](around:{radius},{latitude},{longitude});
        );
        out center;
        """

        response = requests.get(overpass_url, params={"data": overpass_query})
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        hospitals = []
        for element in data.get("elements", []):
            name = element.get("tags", {}).get("name", "Unknown Hospital")
            lat = element.get("lat", element.get("center", {}).get("lat"))
            lon = element.get("lon", element.get("center", {}).get("lon"))

            if lat and lon:
                hospitals.append({"name": name, "latitude": lat, "longitude": lon})

        return hospitals if hospitals else f"No hospitals found near postal code: {postal_code}."

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "Could not connect to the map service. Please try again later."
    except Exception as e:
        print(f"An unexpected error occurred in find_hospitals_osm: {e}")
        return "An unexpected error occurred while finding hospitals."

