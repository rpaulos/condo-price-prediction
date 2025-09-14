import streamlit as st
from streamlit_folium import st_folium
import folium
import functions

st.set_page_config(layout="wide")

# --- Initialize session state for map center and zoom ---
if "map_lat" not in st.session_state:
    st.session_state.map_lat = 14.6760
    st.session_state.map_lon = 121.0437
if "zoom" not in st.session_state:
    st.session_state.zoom = 13

logo_image = "Assets/logo.png"
st.sidebar.image(logo_image)
st.sidebar.title("Options")

condo_name = st.sidebar.text_input("Enter your condo name:")
neighborhood = st.sidebar.selectbox(
    "Select your neighborhood:",
    ["Cubao", "Fairview", "Novaliches", "Diliman", "Tandang Sora"]
)
submit = st.sidebar.button("Submit")

# --- Update session state if user submits ---
if submit and condo_name:
    coords = functions.get_coordinates(condo_name, neighborhood)
    if coords:
        st.session_state.map_lat, st.session_state.map_lon = coords
        st.session_state.zoom = 16
    else:
        st.sidebar.error("No location found for that condo and neighborhood.")

m = functions.build_map(st.session_state.map_lat, st.session_state.map_lon, st.session_state.zoom, condo_name, submit)

nearby_establishments = functions.get_nearby_establishments(st.session_state.map_lat, st.session_state.map_lon)

print(nearby_establishments)

m = functions.pin_establishments_to_map(m, nearby_establishments)

st.title("Quezon City")
st_folium(m, height=600, use_container_width=True)