import googlemaps
import folium
import streamlit as st

from keys import googlemaps_api_key
from typing import List, Dict, Optional

gmaps = googlemaps.Client(key=googlemaps_api_key)

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

    # Marker for current location
    folium.Marker(
        [st.session_state.map_lat, st.session_state.map_lon],
        popup=condo_name if submit and condo_name else "Quezon City",
        tooltip="Click for info"
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

