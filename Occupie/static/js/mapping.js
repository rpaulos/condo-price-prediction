    // Declare global variables
    let map;
    let geocoder;
    let marker;
    let circle;
    let resultsData = [];
    let nearbyMarkers = [];

    const tags = [
        "school", "hospital", "shopping_mall", "supermarket", "church",
        "park", "gym", "restaurant", "bank", "pharmacy", "police",
        "subway_station", "train_station", "university",
        "transit_station", "bus_station"
    ];

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

        geocoder.geocode({ address: address }, async (results, status) => {
            if (status === "OK") {
                const location = results[0].geometry.location;
                map.setCenter(location);

                if (marker) marker.setMap(null);
                nearbyMarkers.forEach(m => m.setMap(null));
                nearbyMarkers = [];

                marker = new google.maps.Marker({
                    map: map,
                    position: location,
                });

                if (circle) circle.setMap(null);
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

                resultsData = [];

                for (const tag of tags) {
                    await nearbySearch(location, tag);
                }

                console.log("All results:", resultsData);
            } else {
                alert("Geocode was not successful: " + status);
            }
        });
    }

    async function nearbySearch(location, tag) {
        const { Place } = await google.maps.importLibrary("places");

        const request = {
            fields: ["displayName", "location"],
            locationRestriction: {
                center: location,
                radius: 500,
            },
            includedTypes: [tag],
        };

        try {
            const { places } = await Place.searchNearby(request);

            if (!places || places.length === 0) return;

            places.forEach(place => {
                const m = new google.maps.Marker({
                    map: map,
                    position: place.location,
                    icon: { url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png" },
                });

                nearbyMarkers.push(m);

                resultsData.push({
                    tag: tag,
                    name: place.displayName,
                    lat: place.location.lat,
                    lng: place.location.lng,
                });
            });
        } catch (err) {
            console.error("Nearby search failed for", tag, err);
        }
    }

    // Form submission
    document.getElementById('valuationForm').addEventListener('submit', function(e) {
        e.preventDefault();
        searchLocation();

        document.body.style.cursor = 'wait';

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
        .catch(err => console.error(err))
        .finally(() => {
            document.body.style.cursor = 'default';
        })
    });
});