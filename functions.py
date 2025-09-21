import googlemaps
import folium
import pickle

import streamlit as st
import pandas as pd
import google.generativeai as genai

from keys import googlemaps_api_key, gemini_api_key
from typing import List, Dict, Optional

gmaps = googlemaps.Client(key=googlemaps_api_key)
genai.configure(api_key=gemini_api_key)

def get_coordinates(condo: str, neighborhood: str) -> tuple[float, float] | None:
    # Returns (lat, lon) of the first matching place or None if no results.

    query = f"{condo}, {neighborhood}, Quezon City, Philippines"
    places = gmaps.places(query)
    if places["results"]:
        loc = places["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None

def build_map(lat: float, lon: float, zoom: int, condo_name: str, submit: bool) -> folium.Map:
    # Builds and returns a folium map centered at (lat, lon) with the given zoom level.

    m = folium.Map(
        location=[lat, lon],
        zoom_start=st.session_state.zoom,
        tiles="OpenStreetMap"
    )

    condo_icon_path = "Assets/condo.png"
    # Marker for current location
    folium.Marker(
        [st.session_state.map_lat, st.session_state.map_lon],
        popup=condo_name if submit and condo_name else "Quezon City",
        tooltip="Click for info",
        icon=folium.CustomIcon(icon_image=condo_icon_path, icon_size=(30, 30))
    ).add_to(m)

    # Draw radius only if user has successfully searched
    if st.session_state.zoom == 16:
        folium.Circle(
            radius=500,
            location=[st.session_state.map_lat, st.session_state.map_lon],
            color="blue",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

    return m

def get_nearby_establishments(lat: float, lon: float, radius: int = 500) -> list[dict]:
    # Returns a list of nearby establishments within the specified radius (in meters).
    nearby_establishments = []

    tags = ["school", "hospital", "shopping_mall", "supermarket", "church", 
            "park", "gym", "restaurant", "bank", 
            "pharmacy", "police", "subway_station", "train_station", "university",
            "transit_station", "bus_station"]
    
    tag_colors = {
        'school':          'darkgreen',
        'hospital':        'red',
        'shopping_mall':   'purple',
        'supermarket':     'green',
        'church':          'darkred',
        'park':            'lightgreen',
        'gym':             'orange',
        'restaurant':      'pink',
        'bank':            'darkblue',
        'pharmacy':        'cadetblue',
        'police':          'black',
        'subway_station':  'lightblue',
        'train_station':   'darkpurple',
        'university':      'beige',
        'transit_station': 'gray',
        'bus_station':     'lightgray'
    }
    
    for tag in tags:
        places_result = gmaps.places_nearby(location=(lat, lon), radius=radius, type=tag)
        nearby_establishments.extend(places_result.get("results", []))

        for places in places_result['results']:
            establishment_name = places['name']
            latitude = places['geometry']['location']['lat']
            longitude = places['geometry']['location']['lng']

            if tag in tag_colors:
                color = tag_colors[tag]
            else:
                color = 'blue'

            nearby_establishments.append({
                'tag': tag,
                'name': establishment_name,
                'latitude': latitude,
                'longitude': longitude,
                'pin_color': color
            })
    
    return nearby_establishments

def pin_establishments_to_map(m: folium.Map, establishments: List[Dict[str, Optional[str]]]) -> folium.Map:

    for est in establishments:
        lat = est.get('latitude')
        lon = est.get('longitude')
        name = est.get('name')
        color = est.get('pin_color', 'blue')

        if lat is not None and lon is not None:
            folium.Marker(
                location=[lat, lon],
                popup=name,
                icon=folium.Icon(color=color)
            ).add_to(m)

    return m

# Get the latitude and longitude
def reverse_geocode(condo_name, neighborhood):
    full_address = f'{condo_name}, {neighborhood}, Quezon City, Philippines'

    try:
        geocode_results = gmaps.geocode(full_address)
    except Exception as e:
        print('Geocoding error: ', e)
        return None, None

    if geocode_results:
        location = geocode_results[0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        lat, lng = None, None

# Get the PlaceID and the geolocation
def place(condo_name, neighborhood):
    gmaps = googlemaps.Client(googlemaps_api_key)
    
    query = f'{condo_name}, {neighborhood}, Quezon City, Philippines'

    results = gmaps.find_place(
        input=query,
        input_type='textquery',
        fields=['place_id', 'geometry']
    )

    if results['candidates']:
        candidate = results['candidates'][0]
        place_id = candidate['place_id']
        lat = candidate['geometry']['location']['lat']
        lng = candidate['geometry']['location']['lng']

        return place_id, lat, lng
    
    return None, None, None


# Get the ratings and number of ratings
def places_details(place_ID):
    details = gmaps.place(
        place_id=place_ID,
        fields=['rating', 'user_ratings_total']
    )
    
    if 'result' in details:
        rating = details['result'].get('rating')
        rating_count = details['result'].get('user_ratings_total')

        return rating, rating_count
    
    return None, None

# Format the data to feed the multiple linear regression model
def format_data(furnishing, bedrooms, bathrooms, amenities, ratings, review_count, size):
    bedrooms = int(bedrooms)
    bathrooms = int(bathrooms)
    size = float(size)
    ratings = float(ratings) if ratings is not None else 0.0
    review_count = int(review_count) if review_count is not None else 0

    amenities_count = len(amenities)

    Security = 1 if 'Security' in amenities else 0
    Airconditioning = 1 if 'Airconditioning' in amenities else 0
    Parking = 1 if 'Parking' in amenities else 0
    Balcony = 1 if 'Balcony' in amenities else 0
    Study_Hall = 1 if 'Study Hall' in amenities else 0
    Swimming_pool = 1 if 'Swimming Pool' in amenities else 0
    Multi_Purpose_Hall = 1 if 'Multi-Purpose Hall' in amenities else 0
    Function_Room = 1 if 'Function Rooms' in amenities else 0
    Gym = 1 if 'Gym' in amenities else 0

    if furnishing == 'Unfurnished':
        furnishing = 0
    elif furnishing == 'Semi Furnished':
        furnishing = 1
    elif furnishing == 'Fully Furnished':
        furnishing = 2

    if (size <= 30):
        size_category = 0
    elif (size <= 50):
        size_category = 1
    elif (size <= 75):
        size_category = 2
    else:
        size_category = 3

    features = pd.DataFrame([{
        "Square Area": size,
        "Bedrooms": bedrooms,
        "Bathrooms": bathrooms,
        "Security": Security,
        "Airconditioning": Airconditioning,
        "Parking": Parking,
        "Balcony": Balcony,
        # "Rating": ratings,
        # "ReviewsCount": review_count,
        "Swimming pool": Swimming_pool,
        "Multi-Purpose Hall": Multi_Purpose_Hall,
        "Function Rooms": Function_Room,
        "Gym": Gym,
        "Study Hall": Study_Hall,
        "furnishing_label": furnishing,
        "amenities_count": amenities_count,
        "size_category": size_category
    }])

    features.insert(0, "const", 1.0)

    return features

# # Get the nearby establishments
# def nearby_search(lat: float, lon: float) -> list[dict]:
#     radius = 500
#     nearby_establishments = []

#     tags= {
#         'school', 'hospital', 'shopping_mall', 'supermarket', 'church',
#         'park', 'gym', 'restaurants', 'bank', 'pharmacy', 'police',
#         'subway_station', 'train_station', 'university', 
#         'transit_station', 'bus_station'
#     }

#     tag_colors = {
#         'school':          'darkgreen',
#         'hospital':        'red',
#         'shopping_mall':   'purple',
#         'supermarket':     'green',
#         'church':          'darkred',
#         'park':            'lightgreen',
#         'gym':             'orange',
#         'restaurant':      'pink',
#         'bank':            'darkblue',
#         'pharmacy':        'cadetblue',
#         'police':          'black',
#         'subway_station':  'lightblue',
#         'train_station':   'darkpurple',
#         'university':      'beige',
#         'transit_station': 'gray',
#         'bus_station':     'lightgray'
#     }

#     for tag in tags:
#         places_result = gmaps.places_nearby(
#             location=(lat, lon),
#             radius=radius,
#             type=tag
#         )

#         for place in places_result.get('results', []):
#             nearby_establishments.append({
#                 'tag': tag,
#                 'name': place['name'],
#                 'latitude': place['geometry']['location']['lat'],
#                 'longitude': place['geometry']['location']['lng'],
#                 'pin_color': tag_colors.get(tag, 'blue')
#             })

#     return nearby_establishments

# Get the establishments nearby the condo
def nearby_establishment_search(lat: float, lng: float) -> list[dict]:

    radius = 500
    nearby_establishments = []
    place_ids = set()

    tags= {
        'school', 'hospital', 'shopping_mall', 'supermarket', 'church',
        'park', 'gym', 'restaurant', 'bank', 'pharmacy', 'police',
        'subway_station', 'train_station', 'university', 
        'transit_station', 'bus_station'
    }

    for tag in tags:
        places_results = gmaps.places_nearby(
            location=(lat, lng),
            radius=radius,
            type=tag
        )

        for place in places_results.get('results', []):
            place_id = place['place_id']

            if place_id in place_ids:
                continue

            nearby_establishments.append({
                'place_id': place_id,
                'type': tag,
                'name': place['name'],
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng']
            })
            place_ids.add(place_id)

    return nearby_establishments

# Format the query to pass to Gemini
def justification_query(condo_name, neighborhood, size, bedrooms, bathrooms, furnishing, amenities, establishments, predicted_price):

    predicted_price = predicted_price[0]

    query = {
        'condo_name': condo_name,
        'neighborhood': neighborhood,
        'size_sqm': size,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'furnishing': furnishing,
        'amenities': amenities,
        'nearby_places': establishments,
        'predicted_price': predicted_price
    }
    return query

# Multiple Linear Regression Model
def multiple_linear_regression_model(formatted_data):
    with open('mlr_model2.pkl', 'rb') as f:
        model = pickle.load(f)

    predictiction = model.predict(formatted_data)
    print(predictiction)

    return predictiction

# Logistic Regression Model
def logistic_regression_model(formatted_data):
    with open('lr_model2.pkl', 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict(formatted_data.values)
    probability = model.predict_proba(formatted_data.values
                                      )
    print('Prediction: ', prediction)
    print('Probability: ', probability)

    return prediction, probability

def justify_condo_price(
    condo_name: str,
    neighborhood: str,
    size_sqm: float,
    bedrooms: int,
    bathrooms: int,
    furnishing: str,
    amenities: List[str],
    nearby_places: List[Dict[str, str]],
    predicted_price: float
) -> str:
    """
    Calls Google Gemini to generate a professional property price justification.

    Args:
        condo_name (str): Name of the condo.
        neighborhood (str): Location/neighborhood of the condo.
        size_sqm (float): Area in square meters.
        bedrooms (int): Number of bedrooms.
        bathrooms (int): Number of bathrooms.
        furnishing (str): Furnishing status (e.g., "Semi-Furnished").
        amenities (List[str]): List of condo amenities.
        nearby_places (List[Dict[str, str]]): List of nearby places, each as {'type': 'school', 'name': 'ABC School'}.
        predicted_price (float): Predicted price of the condo.

    Returns:
        str: AI-generated justification for the condo price.
    """

    nearby_summary = ", ".join([f"{p['name']} ({p['type']})" for p in nearby_places])
    amenities_summary = ", ".join(amenities)

    prompt = f"""
You are an experienced real estate analyst based in Quezon City, Philippines.
A condo has the following details:

- Name: {condo_name}
- Neighborhood: {neighborhood}
- Size: {size_sqm} sqm
- Bedrooms: {bedrooms}
- Bathrooms: {bathrooms}
- Furnishing: {furnishing}
- Amenities: {amenities_summary}
- Nearby establishments: {nearby_summary}

The predicted price is {predicted_price:,.2f} in Philippine Peso.

Your job is to provide a concise, professional justification for this price based on the condo features, amenities, and nearby establishments.
Highlight why the location, amenities, or features may increase or decrease its value.

"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    # response = genai.chat.create(
    #     model='',
    #     messages=[{'author': 'user', 'content': prompt}],
    #     temperature=0.7
    # )

    # justification = response.last.split('\n')[0] if hasattr(response, 'last') else response.output[0].content
    return response.text