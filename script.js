// JavaScript for handling the tab system
const tabs = {
    home: "content",
    about: "about-tab",
    contact: "contact-tab",
    map: "map-tab",
    signin: "signin-tab",
};

document.querySelector("nav").addEventListener("click", (event) => {
    if (event.target.tagName === "A") {
        event.preventDefault();
        for (const tab in tabs) {
            if (tab === event.target.getAttribute("href").substring(1)) {
                document.getElementById(tabs[tab]).style.display = "block";
                if (tab === "map") {
                    // Check if the map is already initialized
                    if (!map) {
                        initMap();
                    }
                }
            } else {
                document.getElementById(tabs[tab]).style.display = "none";
            }
        }
    }
});
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
async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    map = new Map(mapContainer, {
        center: { lat: 38.9, lng: -77.0 },
        restriction: {
            latLngBounds: {north: 40.0, south: 37.0, west: -77.0, east: -75.0},
            strictBounds: false,
          },
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

// Google Sign-In Callback
function onSignIn(googleUser) {
    // Handle the sign-in logic here
    console.log("User is signed in.");
}
// JavaScript for handling Google Sign-In using One Tap
window.onload = function () {
    google.accounts.id.initialize({
        client_id: "221198763427-g67flvpi5mfvqlhh0a2je4517io0ngkc.apps.googleusercontent.com", // Replace with your client ID
        callback: handleCredentialResponse
    });
    google.accounts.id.renderButton(
        document.getElementById("buttonDiv"),
        { theme: "outline", size: "large" }
    );
    google.accounts.id.prompt();
}

function handleCredentialResponse(response) {
    // Handle the Google Sign-In response here
    // Typically, you would send this response to your server for verification
    console.log("Encoded JWT ID token: " + response.credential);
}

document.addEventListener("DOMContentLoaded", function () {
    const contactTab = document.getElementById("contact-tab");
    const showContactFormButton = document.getElementById("show-contact-form-button");
    const contactForm = document.getElementById("contact-form");

    // Show the contact form when the button is clicked
    showContactFormButton.addEventListener("click", function () {
        showContactFormButton.style.display = "none";
        contactForm.style.display = "block";
    });

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

        // Simulate form submission (adjust this part for your server)
        // Assuming a successful submission
        simulateFormSubmission(contactData);
    });

    function simulateFormSubmission(contactData) {
        // Send contactData to the server for saving (simulated with a delay)
        setTimeout(() => {
            // Reset the form
            document.getElementById("name").value = "";
            document.getElementById("email").value = "";
            document.getElementById("message").value = "";

            // Show success message and hide the form
            alert("Contact form submitted successfully!");
            contactTab.style.display = "none";
            showContactFormButton.style.display = "block";
        }, 1000); // Simulated submission delay (1 second)
    }
}); 