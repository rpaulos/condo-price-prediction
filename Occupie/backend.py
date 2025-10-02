import googlemaps
import requests
import markdown

import numpy as np

from flask import Flask, jsonify, request, render_template
from keys import googlemaps_api_key
from functions import reverse_geocode, nearby_establishment_search, count_categories, place, places_details, format_data, format_data_lr, multiple_linear_regression_model, logistic_regression_model, justification_query, justify_condo_price
from akasha import send_user_message, justify_condo_price_chat
from pprint import pprint

app = Flask(__name__)

latest_results = {}
chat_history = []

condo_name = None
neighborhood = None
size = None
bedrooms = None
bathrooms = None
furnishing = None
amenities = None
establishments = None
predicted_price = None
predicted_occupancy = None

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/occupie', methods=['GET', 'POST'])
def valuation():
    return render_template('occupie.html')

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/submit', methods=['POST'])
def occupie():
    global condo_name, neighborhood, size, bedrooms, bathrooms, furnishing, amenities, establishments, predicted_price, predicted_occupancy

    condo_name = request.form.get('name-of-condo')
    neighborhood = request.form.get('neighborhood')
    furnishing = request.form.get('type-of-furnishing')
    size = request.form.get('size-of-condo')
    bedrooms    = request.form.get('count-of-bedrooms')
    bathrooms   = request.form.get('count-of-bathrooms')
    amenities   = request.form.getlist('amenities')

    # if not condo_name and not neighborhood:
    #     condo_name = 'Quezon City, Philippines'
    # elif not condo_name:
    #     condo_name = f'{neighborhood}, Quezon City, Philippines'
    # elif not neighborhood:
    #     condo_name = f'{condo_name}, Quezon City, Philippines'

    # Reverse geocode the location of the condo and its unique place_ID
    city, place_ID, lat, lng = place(condo_name, neighborhood)

    print(city)

    if city and 'quezon' in city.lower():
        # Get the reviews and the number of reviews
        ratings, review_count = places_details(place_ID)

        # Locate the establishments within a 500 meter radius
        establishments = nearby_establishment_search(lat, lng)

        transportation_count, healthcare_count, education_count, shopping_count, restaurants_count = count_categories(establishments)

        # Format the data to pass to the price predictor model
        formatted_data_mlr = format_data(furnishing, bedrooms, bathrooms, amenities, ratings, review_count, size)

        # Pass the formatted data to the ML model to get the predicted price
        predicted_price = multiple_linear_regression_model(formatted_data_mlr)
        # predicted_price = float(predicted_price)

        formatted_data_lr = format_data_lr(formatted_data_mlr, predicted_price)

        # Pass the formatted data with the result from the MLR model to get the occupancy rate
        predicted_occupancy, probability = logistic_regression_model(formatted_data_lr)
        predicted_occupancy = str(predicted_occupancy)

        # Formate the data needed to annalyze the results
        prompt = justification_query(condo_name, neighborhood, size, bedrooms, bathrooms, furnishing, amenities, establishments, predicted_price, predicted_occupancy)

        # Pass the prompt to Gemini to analyze the result
        ai_analysis = justify_condo_price(**prompt)
        markdown_ai_analysis = markdown.markdown(ai_analysis)

        return jsonify({
            'predicted_price': predicted_price,
            'predicted_occupancy': predicted_occupancy,
            'transportation_count': transportation_count,
            'healthcare_count': healthcare_count,
            'education_count': education_count,
            'shopping_count': shopping_count,
            'restaurant_count': restaurants_count,
            'markdown_ai_analysis': markdown_ai_analysis
        })

    else: 
        print('You have reached this')
        return jsonify({
            'predicted_price': 0,
            'predicted_occupancy': 0,
            'transportation_count': 0,
            'healthcare_count': 0,
            'education_count': 0,
            'shopping_count': 0,
            'restaurant_count': 0,
            'markdown_ai_analysis': 'Location is outside of Quezon City. No analysis available.',
            'note': 'Fallback values returned because the location is not in Quezon City.'
        }), 200 


@app.route('/ask-akasha', methods=['POST'])
def akasha():
    user_message = request.form.get("akasha-terminal-input-field")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    akasha_response = send_user_message(user_message)

    if not akasha_response:
        akasha_response = "Sorry, I didn’t understand that."

    # print("Akasha responding with:", akasha_response)
    # print("Chat history:", chat_history)

    akasha_response_html = markdown.markdown(akasha_response)


    chat_history.append({'user': user_message, 'akasha': akasha_response_html})

    # return render_template("occupie.html", akasha_response=akasha_response)

    return jsonify({
        'chat_history': chat_history,
        'akasha_response': akasha_response_html
    })


if __name__ == "__main__":
    app.run(debug=True)
