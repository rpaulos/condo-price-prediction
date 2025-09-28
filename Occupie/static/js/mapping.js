// Declare global variables
let map;
let geocoder;
let marker;
let circle;
let resultsData = [];
let nearbyMarkers = [];

const tags = [
    // Restaurants
    "restaurant",

    // Shopping
    "shopping_mall",
    "supermarket",

    // Education
    "school",
    "university",

    // Transporation
    "subway_station",
    "train_station",
    "transit_station",
    "bus_station",

    // Healthcare
    "hospital",
    "pharmacy",

    // Others
    "bank",
    "church",
    "park",
    "police",
    "gym"
];

const category_mapping = {
    // Restaurants
    'restaurant': 'Restaurants',

    // Shopping
    'shopping_mall': 'Shopping',
    'supermarket': 'Shopping',

    // Education
    'school': 'Education',
    'university': 'Education',

    // Transportation
    'train_station': 'Transportation',
    'bus_station': 'Transportation',
    'subway_station': 'Transportation',
    'transit_station': 'Transportation',

    // Healthcare
    'hospital': 'Healthcare',
    'pharmacy': 'Healthcare',

    // Others
    'bank': 'Others',
    'police': 'Others',
    'park': 'Others',
    'church': 'Others',
    'gym': 'Others',
};

const category_colors = {
    'Transportation': 'yellow',
    'Healthcare': 'green',
    'Education': 'orange',
    'Shopping': 'purple',
    'Restaurants': 'blue',
    'Others': 'pink'
};

// This function is called by Google Maps API after it loads
window.initMap = function() {
    map = new google.maps.Map(document.getElementById("map-container"), {
        center: { lat: 14.61286, lng: 121.05457 },
        zoom: 15,
    });
    geocoder = new google.maps.Geocoder();
};

document.addEventListener('DOMContentLoaded', function() {

    function searchLocation() {
        const condo_name = document.getElementById("name-of-condo").value;
        const neighborhood = document.getElementById("neighborhood").value;

        if (!condo_name && !neighborhood) {
            address = "Quezon City, Philippines"
        } else if (!condo_name) {
            address = `${neighborhood}, Quezon City, Philippines`;
        } else if (!neighborhood) {
            address = condo_name;
        } else {
            address = `${condo_name}, ${neighborhood}, Quezon City, Philippines`;
        }

        if (condo_name && neighborhood) {
            address = `${condo_name}, ${neighborhood}, Quezon City, Philippines`;

        } else if (neighborhood) {// condo_name is empty, neighborhood is not
            address = `${neighborhood}, Quezon City, Philippines`;

        } else if (condo_name) { // neighborhood is empty, condo_name is not
            address = condo_name;

        } else { // both are empty
            address = "Cubao, Quezon City, Philippines"
        }
        
        // const address = `${condo_name}, ${neighborhood}, Quezon City, Philippines`;

        if (!geocoder) {
            alert("Google Maps API is still loading. Try again.");
            return;
        }

        // Use the Google Maps Geocoder to convert a text address into geographic coordinates
        geocoder.geocode({ address: address }, async (results, status) => {
            // Check if the geocoding request was successful
            if (status === "OK") {
                // Extract the geographic location (latitude and longitude) from the first result
                const location = results[0].geometry.location;

                // Center the map on the geocoded location
                map.setCenter(location);

                // Remove the previous single marker if it exists
                if (marker) marker.setMap(null);

                // Clear all existing nearby markers from the map
                nearbyMarkers.forEach(m => m.setMap(null));
                nearbyMarkers = [];

                // Place a new marker at the geocoded location
                marker = new google.maps.Marker({
                    map: map,
                    position: location,
                });

                // Remove any existing circle on the map
                if (circle) circle.setMap(null);

                // Draw a new circle with a 500-meter radius around the geocoded location
                circle = new google.maps.Circle({
                    map: map,
                    radius: 500,
                    fillColor: "#00AAFF",
                    fillOpacity: 0.15,
                    strokeColor: "#0088CC",
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    center: location,
                });

                // Reset the array holding the search results
                resultsData = [];

                // For each tag type, perform a nearby search and wait for it to complete
                for (const tag of tags) {
                    await nearbySearch(location, tag);
                }

                // Log all the gathered results for debugging or further processing
                console.log("All results:", resultsData);
            } else {
                // Show an alert if the geocoding request was not successful
                alert("Geocode was not successful: " + status);
            }
        });
    }

    // Asynchronous function to search for nearby places of a given type (tag) around a location
    async function nearbySearch(location, tag) {
        // Import the Google Maps Places library
        const { Place } = await google.maps.importLibrary("places");

        // Prep the request object for the Places API
        const request = {
            // Specify which fields to return for each place
            fields: ["displayName", "location"],
            locationRestriction: {
                // Define the search area as a circle with a 500m radius around the given location
                center: location,
                radius: 500,
            },
            // Filter results to include only places matching the provided tag (type)
            includedTypes: [tag],
        };

        try {
            // Perform a nearby search using the prepared request
            const { places } = await Place.searchNearby(request);

            // If no places are found, exit the function early
            if (!places || places.length === 0) return;

            const category = category_mapping[tag] || 'Others';
            const color = category_colors[category] || 'blue';

            // Loop through each returned place
            places.forEach(place => {
                // Create a blue marker on the map at the place's location
                const m = new google.maps.Marker({
                    map: map,
                    position: place.location,
                    icon: { 
                        url: `http://maps.google.com/mapfiles/ms/icons/${color}-dot.png` 
                    },
                });

                // Store the created marker in the nearbyMarkers array for later reference
                nearbyMarkers.push(m);

                // Add the place information to resultsData for further processing or display
                resultsData.push({
                    tag: tag,
                    name: place.displayName,
                    lat: place.location.lat,
                    lng: place.location.lng,
                });
            });
        } catch (err) {
            // Log an error message if the nearby search fails
            console.error("Nearby search failed for", tag, err);
        }
    }

    // Form submission
    document.getElementById('valuationForm').addEventListener('submit', function(e) {
        // Prevent the default form submission to handle it via JavaScript
        e.preventDefault();

        // Trigger the function to search for the location on the map
        searchLocation();

        // Change the cursor to a "wait" (loading) icon while the request is being processed
        document.body.style.cursor = 'wait';

        // Send the form data to the server endpoint '/submit' using a POST request
        fetch('/submit', {
            method: 'POST',
            body: new FormData(this)
        })
        .then(res => res.json())
        .then(data => {
            console.log("Server response:", data);
            console.log("Predicted occupancy:", data.predicted_occupancy);

            // Update the predicted price and occupancy
            document.getElementById('monthly-rent-prediction').innerText = Number(data.predicted_price).toFixed(2);
            document.getElementById('demand-prediction').innerText = String(data.predicted_occupancy);

            // Update the nearby establishments count
            document.getElementById('nearby-education').innerText = data.education_count;
            document.getElementById('nearby-shopping').innerText = data.shopping_count;
            document.getElementById('nearby-transportation').innerText = data.transportation_count;
            document.getElementById('nearby-healthcare').innerText = data.healthcare_count;
            document.getElementById('nearby-restaurant').innerText = data.restaurant_count;

            // Update the AI analysis text
            console.log("AI HTML content:", data.markdown_ai_analysis);
            document.getElementById('ai-analysis-text').innerHTML = data.markdown_ai_analysis;

            console.log("Updated counts:", {
                education: data.education_count,
                shopping: data.shopping_count,
                transportation: data.transportation_count,
                healthcare: data.healthcare_count,
                restaurant: data.restaurant_count
            });
        })
        // Log any errors if the fetch request fails
        .catch(err => console.error(err))
        .finally(() => {
            // Restore the cursor to its default state once processing is done
            document.body.style.cursor = 'default';
        })
    });
});