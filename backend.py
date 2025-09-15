from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/valuation')
def valuation():
    return render_template('valuation.html')

@app.route('/submit', methods=['POST'])
def submit():
    condo_name  = request.form.get('condo-name')
    neighborhood = request.form.get('neighborhood')
    bedrooms    = request.form.get('bedrooms')
    bathrooms   = request.form.get('bathrooms')
    amenities   = request.form.getlist('amenities')

    return render_template(
        'valuation.html',
        success_message="Your details have been submitted!"
    )

    # return f"""
    #     Condo Name: {condo_name}<br>
    #     Neighborhood: {neighborhood}<br>
    #     Bedrooms: {bedrooms}<br>
    #     Bathrooms: {bathrooms}<br>
    #     Amenities: {', '.join(amenities)}
    # """

if __name__ == "__main__":
    app.run(debug=True)