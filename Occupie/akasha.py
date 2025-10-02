import google.generativeai as genai
from typing import List, Dict
from keys import gemini_api_key

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

chat = model.start_chat(history=[
    {'role': 'user', 'parts': [
        'Your name is Akasha'
        'You are an experienced real estate analyst based in Quezon City, Philippines.'
        'You are knowledgeable in market trends in real estate'
        'Your task is to explain condo prices, occupancy, and market factors in a professional yet conversational tone.'
        'Never answer questions that are not related to real estate'
        'If the user asks about non related topics, reply with that is outside of my scope.'
        'If the user greets your, respond politely and ask them how you can help.'
        'Introduce yourself as Akasha AI'
    ]}
])

def send_user_message(message: str) -> str:
    '''
    Sends a free form message to the chatbot (user side).
    '''

    response = chat.send_message(message)
    return response.text

def justify_condo_price_chat(
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
    '''
    Structured condo justification requests with context saved in chat history.
    '''

    nearby_summary = ', '.join([f"{p['name']} ({p['type']})" for p in nearby_places])
    amenities_summary =', '.join(amenities)

    prompt = f"""
A condo has the following details:

- Name: {condo_name} (Based on the details, create a flowery descriptive name for the condo unit)
- Neighborhood: {neighborhood}
- Size: {size_sqm} sqm
- Bedrooms: {bedrooms}
- Bathrooms: {bathrooms}
- Furnishing: {furnishing}
- Amenities: {amenities_summary}
- Nearby Establishments: {nearby_summary}

Predicted Price: {predicted_price:,.2f} PHP
Predicted Occupancy: {predicted_occupancy}

Provide analysis in valid HTML with the following structure:

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

"""
    
    response = chat.send_message(prompt)
    return response.text

# print("booting up jarvis")

# html_response = justify_condo_price_chat(
#     "Skyline Towers", "Quezon City", 80, 2, 2, "Fully Furnished",
#     ["Swimming Pool", "Gym", "Playground"],
#     [{"type": "school", "name": "ABC University"}, {"type": "mall", "name": "SM North"}],
#     8500000, "High"
# )

# print(html_response)

# print(send_user_message("Hello, my name is Rae, what is your name?"))


