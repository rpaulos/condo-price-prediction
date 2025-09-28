import googlemaps
import folium
import pickle

import streamlit as st
import numpy as np
import pandas as pd
import google.generativeai as genai

from keys import googlemaps_api_key, gemini_api_key
from typing import List, Dict, Optional

gmaps = googlemaps.Client(key=googlemaps_api_key)
genai.configure(api_key=gemini_api_key)

# Streamlit
def get_coordinates(condo: str, neighborhood: str) -> tuple[float, float] | None:
    # Returns (lat, lon) of the first matching place or None if no results.

    query = f"{condo}, {neighborhood}, Quezon City, Philippines"
    places = gmaps.places(query)
    if places["results"]:
        loc = places["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None

# Streamlit
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

# Streamlit
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

# Streamlit
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
    
    # if not condo_name:
    #     query = f'{neighborhood}, Quezon City, Philippines'
    # else:
    #     query = f'{condo_name}, {neighborhood}, Quezon City, Philippines'

    if condo_name and neighborhood:
        address = f"{condo_name}, {neighborhood}, Quezon City, Philippines"

    elif neighborhood:  # condo_name is empty, neighborhood is not
        address = f"{neighborhood}, Quezon City, Philippines"

    elif condo_name:    # neighborhood is empty, condo_name is not
        address = condo_name

    else:
        address = "Cubao, Quezon City, Philippines"


    results = gmaps.find_place(
        input=address,
        input_type='textquery',
        fields=['place_id', 'geometry']
    )

    if results['candidates']:
        candidate = results['candidates'][0]
        place_id = candidate['place_id']
        lat = candidate['geometry']['location']['lat']
        lng = candidate['geometry']['location']['lng']

        rev = gmaps.reverse_geocode((lat, lng))
        city = None
        country = None
        if rev:
            for comp in rev[0]['address_components']:
                if 'locality' in comp['types']:
                    city = comp['long_name'].lower()
                    break

        return city, place_id, lat, lng
    
    return None, None, None, None


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
    # ratings = float(ratings) if ratings is not None else 0.0
    # review_count = int(review_count) if review_count is not None else 0

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

def format_data_lr(features, predicted_price):
    features['Price'] = predicted_price
    features = features.drop(columns=['const'])

    features = features.astype('int64')

    print(features['Square Area'])
    print(features['Bedrooms'])
    print(features['Bathrooms'])
    print(features['Security'])
    print(features['Airconditioning'])
    print(features['Parking'])
    print(features['Balcony'])
    print(features['Swimming pool'])
    print(features['Multi-Purpose Hall'])
    print(features['Function Rooms'])
    print(features['Gym'])
    print(features['Study Hall'])
    print(features['furnishing_label'])
    print(features['amenities_count'])
    print(features['size_category'])
    print(features['Price'])

    return features

# Get the establishments nearby the condo
def nearby_establishment_search(lat: float, lng: float) -> list[dict]:

    radius = 500
    nearby_establishments = []
    place_ids = set()

    tags = {
        # Restaurants
        "restaurant",

        # Shopping
        "shopping_mall",
        "supermarket",

        # Education
        "school",
        "university",

        # Transportation
        "subway_station",
        "train_station",
        "transit_station",
        "bus_station",

        # Healthcare
        "hospital",
        "pharmacy",

        # Others
        "bank",
        "police",
        "park",
        "church",
        "gym",
    }

    category_mapping = {
        # Restaurants
        "restaurant": "Restaurants",

        # Shopping
        "shopping_mall": "Shopping",
        "supermarket": "Shopping",

        # Education
        "school": "Education",
        "university": "Education",

        # Transportation
        "train_station": "Transportation",
        "bus_station": "Transportation",
        "subway_station": "Transportation",
        "transit_station": "Transportation",

        # Healthcare
        "hospital": "Healthcare",
        "pharmacy": "Healthcare",

        # Others
        "bank": "Others",
        "police": "Others",
        "park": "Others",
        "church": "Others",
        "gym": "Others",
    }

    tags = category_mapping.keys()
    counts = {cat: 0 for cat in set(category_mapping.values())}

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

            category = category_mapping.get(tag, 'Other')

            nearby_establishments.append({
                'place_id': place_id,
                'type': tag,
                'category': category,
                'name': place['name'],
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng']
            })
            counts[category] += 1
            place_ids.add(place_id)

    nearby_establishments.append({
        'place_id': None,
        'type': 'counts_summary',
        'category': 'Summary',
        'name': 'Counts by Category',
        'counts': counts
    })

    return nearby_establishments

def count_categories(establishments: list[dict]):
    counts_summary = next((e for e in establishments if e['type'] == 'counts_summary'), None)

    if counts_summary:
        counts = counts_summary['counts']
        transportation_count = counts.get('Transportation', 0)
        healthcare_count = counts.get('Healthcare', 0)
        education_count = counts.get('Education', 0)
        shopping_count = counts.get('Shopping', 0)
        restaurants_count = counts.get('Restaurants', 0)
    else:
        transportation_count = healthcare_count = education_count = shopping_count = restaurants_count = 0

    return transportation_count, healthcare_count, education_count, shopping_count, restaurants_count

# Format the query to pass to Gemini
def justification_query(condo_name, neighborhood, size, bedrooms, bathrooms, furnishing, amenities, establishments, predicted_price, predicted_occupancy):

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
        'predicted_price': predicted_price,
        'predicted_occupancy': predicted_occupancy
    }

    return query

# Multiple Linear Regression Model
def multiple_linear_regression_model(formatted_data):
    with open('mlr_model2.pkl', 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict(formatted_data)

    # prediction = [round(val / 1000) * 1000 for val in prediction]
    
    # Round the prediction result to the nearest thousand
    prediction = np.round(prediction / 1000) * 1000
    
    prediction = prediction.tolist()

    return prediction

# Logistic Regression Model
def logistic_regression_model(formatted_data):
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    with open('lr_model2.pkl', 'rb') as f:
        model = pickle.load(f)

    formatted_data = scaler.transform(formatted_data)

    prediction_array = model.predict(formatted_data)
    probability_array = model.predict_proba(formatted_data)

    print(prediction_array)

    pred_class = prediction_array[0]
    
    if pred_class == 0:
        prediction = 'Low Occupancy'
    elif pred_class == 1:
        prediction = 'Medium Occupancy'
    else:
        prediction = 'High Occupancy'

    probability = probability_array[0]

    print('Prediction: ', prediction)

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
    predicted_price: float,
    predicted_occupancy: str
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
        predicted_occupancy (str): Category of the occupancy rate

    Returns:
        str: AI-generated justification for the condo price.
    """

    nearby_summary = ", ".join([f"{p['name']} ({p['type']})" for p in nearby_places])
    amenities_summary = ", ".join(amenities)

    prompt = f"""
You are an experienced real estate analyst based in Quezon City, Philippines.
A condo has the following details:

- Name: {condo_name} or Create a descriptive and flowery name based on the features of the condo unit (Example: Spacious 2 bedroom 1 bath condo or Spacious family home)
- Neighborhood: {neighborhood}
- Size: {size_sqm} sqm
- Bedrooms: {bedrooms}
- Bathrooms: {bathrooms}
- Furnishing: {furnishing}
- Amenities: {amenities_summary}
- Nearby establishments: {nearby_summary}

The predicted price is {predicted_price:,.2f} in PHP and the predicted occupancy is {predicted_occupancy}.

Provide a professional analysis in the following structured sections, formatted in valid HTML:

<div class=main-ai-analysis-container>
    <div class=title-main-container>
        <div class=title-container>
            <h2>Title of the Summary</h2>
            <h3>Location<h3>
        </div>
    </div>

    <div class=summary-of-results-main-container>
        <p>Brief overview of the condo's value and occupancy rate.</p>
    </div>

    <div class=results-justification-main-container>
        <div class=results-justification-title-container>
            <h2>Explaining the Result</h2>
            <p>Briefly explain the reasons why the condo is valued this way</p>
            <div class=location-influence</div>
                <h3>1. Location Influence</3>
                <p>Briefly explain the influence the location has on the price and occupancy rate.</p>
            </div>
            <div class=amenities-influence>
                <h3>2. Amenities and Features</h3>
                <p>Briefly explain the influence of the amenities and size on the price and occupancy rate.</p>
            </div>
            <div class=nearby-establishments-ai-results>
                <h3>3. Nearby Establishments</h3>
                <p>Briefly explain the influence of the different establishments in the area<p>
                <ul>
                    <li><strong>Education:</strong> Brief explanation<li>
                    <li><strong>Shopping:</strong> Brief explanation<li>
                    <li><strong>Transportation:</strong> Brief explanation<li>
                    <li><strong>Healthcare:</strong> Brief explanation<li>
                    <li><strong>Restaurant:</strong> Brief explanation<li>
                </ul>
            </div>
        </div>
    <div class=recommendations-ai-analysis-main-container>
        <div class=recommendations-ai-analysis>
            <h2>Overall Recommendations</h2>
            <p>Briefly explain how the tenant, user, or landlord can position themselves given the results to maximize the value or leverage the potential occupancy<p>
        </div>
    </div>
</div>

Use proper HTML tags and the given classes. Follow the format above. Do not include markdown or plain text formatting.
Do not include answers that are not relevant to the topic.
"""
    
    # os ng condo low demand, ways to increase the demand

    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)

    return response.text