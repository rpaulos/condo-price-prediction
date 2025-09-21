import googlemaps
import requests
import numpy as np

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from keys import googlemaps_api_key
from functions import reverse_geocode, nearby_establishment_search, place, places_details, format_data, multiple_linear_regression_model, logistic_regression_model, justification_query, justify_condo_price
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
    size = request.form.get('size-of-condo')
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

    # Get the latitude and longitude of the condo
    lat, lng = reverse_geocode(condo_name, neighborhood)

    # Get the unique place ID of the condo and its geolocation
    place_ID, lat, lng = place(condo_name, neighborhood)

    # Get the reviews and the number of reviews
    ratings, review_count = places_details(place_ID)

    # Locate the establishments near the condo
    establishments = nearby_establishment_search(lat, lng)

    # Format the data to pass to the model
    formatted_data = format_data(furnishing, bedrooms, bathrooms, amenities, ratings, review_count, size)

    # Predicted price
    multiple_linear_regression_result = multiple_linear_regression_model(formatted_data)

    # Predicted occupancy
    logistic_regression_results, probability = logistic_regression_model(formatted_data)

    # Transform the mlr result to a list to pass to the model
    predicted_price = multiple_linear_regression_result.tolist()

    # Format the data to pass to the LLM
    query_to_llm = justification_query(condo_name, neighborhood, size, bedrooms, bathrooms, furnishing, amenities, establishments, predicted_price)

    ai_analysis = justify_condo_price(**query_to_llm)

    print(ai_analysis)

    return jsonify({
        'mlr_result': predicted_price,
    })

    # return f"""
    #     Condo Name: {condo_name}<br>
    #     Neighborhood: {neighborhood}<br>
    #     Bedrooms: {bedrooms}<br>
    #     Bathrooms: {bathrooms}<br>
    #     Amenities: {', '.join(amenities)}
    # """

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
