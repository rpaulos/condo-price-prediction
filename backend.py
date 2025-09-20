import googlemaps
import requests

from flask import Flask
from flask import request
from flask import render_template
from keys import googlemaps_api_key
from functions import reverse_geocode, nearby_search
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/valuation')
def valuation():
    return render_template('valuation.html')

@app.route('/submit', methods=['POST'])
def submit():
    condo_name  = request.form.get('name-of-condo')
    neighborhood = request.form.get('neighborhood-location')
    furnishing = request.form.get('type-of-furnishing')
    bedrooms    = request.form.get('count-of-bedrooms')
    bathrooms   = request.form.get('count-of-bathrooms')
    amenities   = request.form.getlist('amenities')

    print("---- Form data received ----")
    print("Condo Name:", condo_name)
    print("Furnishing:", furnishing)
    print("Neighborhood:", neighborhood)
    print("Bedrooms:", bedrooms)
    print("Bathrooms:", bathrooms)
    print("Amenities:", amenities)

    lat, lng = reverse_geocode(condo_name, neighborhood)
    establishments = nearby_search(lat, lng)

    print("Latitude:", lat)
    print("Longitude:", lng)
    pprint(establishments)

    return f"""
        Condo Name: {condo_name}<br>
        Neighborhood: {neighborhood}<br>
        Bedrooms: {bedrooms}<br>
        Bathrooms: {bathrooms}<br>
        Amenities: {', '.join(amenities)}
    """

if __name__ == "__main__":
    app.run(debug=True)


   # lat, lng = reverse_geocode(condo_name, neighborhood)
    # establishments = nearby_search(lat, lng)

    # return render_template(
    #     'valuation.html',
    #     condo_name=condo_name,
    #     neighborhood=neighborhood,
    #     # lat=lat,
    #     # lng=lng,
    #     # establishments=establishments
    # )
