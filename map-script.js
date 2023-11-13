
// In your existing script.js or a new JavaScript file:
document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contact-form");

    contactForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const message = document.getElementById("message").value;

        const contactData = {
            name,
            email,
            message,
        };

        // Send contactData to the server for saving to a JSON file
        fetch("/submitContact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contactData),
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response from the server (e.g., show a success message)
                console.log(data);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    });
});


// JavaScript for handling the map tab
const mapTab = document.getElementById("map-tab");
const addMarkerButton = document.getElementById("add-marker-button");
const mapContainer = document.getElementById("map");
const userMarkerForm = document.getElementById("marker-form");
const addMarkerForm = document.getElementById("add-marker-form");

let map; // Variable to hold the Google Map object
const geocoder = new google.maps.Geocoder();
const markers = [];

// Initialize the map function
function initMap() {
    map = new google.maps.Map(mapContainer, {
        center: { lat: 38.9, lng: -77.0 },
        zoom: 8,
    });

    addMarkerButton.addEventListener("click", () => {
        mapTab.style.display = "none";
        addMarkerForm.style.display = "block";
    });

    // Event listener for the user marker form
    userMarkerForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const address = document.getElementById("address").value;
        const city = document.getElementById("city").value;
        const state = document.getElementById("state").value;
        const zip = document.getElementById("zip").value;
        const fullAddress = `${address}, ${city}, ${state} ${zip}`;

        geocoder.geocode({ address: fullAddress }, (results, status) => {
            if (status === "OK" && results[0].geometry) {
                const position = results[0].geometry.location;
                const markerData = { title, description, position };
                markers.push(markerData);

                // Create a new marker on the map
                const marker = new google.maps.Marker({
                    position,
                    map,
                    title,
                });

                const infowindow = new google.maps.InfoWindow({
                    content: `<h3>${title}</h3><p>${description}</p>`,
                });

                marker.addListener("click", () => {
                    infowindow.open(map, marker);
                });

                userMarkerForm.reset();
                addMarkerForm.style.display = "none";
                mapTab.style.display = "block";
            }
        });
    });
}

// Call the initMap function when the page loads
google.maps.event.addDomListener(window, "load", initMap);

// Function to create markers from widget data
function createMarkersFromData(data) {
    data.forEach((widget) => {
        const position = new google.maps.LatLng(widget.position.lat, widget.position.lng);
        const marker = new google.maps.Marker({
            position,
            map,
            title: widget.title,
        });

        marker.addListener("click", () => {
            infowindow.open(map, marker);
        });
    });
}