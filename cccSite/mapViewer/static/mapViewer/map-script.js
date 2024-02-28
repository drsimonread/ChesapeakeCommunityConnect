document.addEventListener("DOMContentLoaded", function () {
    let map;
    let directionsMap;
    let directionsService;
    let directionsRenderer;

    function initMap() {
        // Initialize the main map
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 38.9, lng: -77.0 },
            zoom: 8,
        });

        // Initialize the secondary map for directions
        directionsMap = new google.maps.Map(document.getElementById("directionsMap"), {
            center: { lat: 38.9, lng: -77.0 },
            zoom: 8,
        });

        // Initialize the directions service and renderer
        directionsService = new google.maps.DirectionsService();
        directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(directionsMap);
    }

    initMap(); // Call the initMap function when the DOM is loaded

    // Add event listeners and other functionalities here
    const addMarkerButton = document.getElementById("add-marker-button");
    const addMarkerForm = document.getElementById("add-marker-form");
    const userMarkerForm = document.getElementById("marker-form");
    const calculateDistanceButton = document.getElementById("calculate-distance");
    const useCurrentLocationButton = document.getElementById("use-current-location");
    const userAddressInput = document.getElementById("user-address");

    // Function to get CSRF token from cookie
    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Event listener for adding markers
    addMarkerButton.addEventListener("click", () => {
        addMarkerForm.style.display = "block";
    });

    // Event listener for submitting marker form
    userMarkerForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const address = document.getElementById("address").value;
        const city = document.getElementById("city").value;
        const state = document.getElementById("state").value;
        const zip = document.getElementById("zip").value;
        const fullAddress = `${address}, ${city}, ${state} ${zip}`;

        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ address: fullAddress }, function (results, status) {
            if (status === 'OK') {
                const position = results[0].geometry.location;
                const marker = new google.maps.Marker({
                    position,
                    map,
                    title: title,
                });

                const infowindow = new google.maps.InfoWindow({
                    content: `<h3>${title}</h3><p>${description}</p>`
                });

                marker.addListener('click', function () {
                    infowindow.open(map, marker);
                });

                map.setCenter(position);
                addMarkerForm.style.display = "none";

                // AJAX call to send data to Django backend
                $.ajax({
                    type: "POST",
                    url: "/save_widget/", // URL of the Django view
                    data: {
                        title: title,
                        description: description,
                        latitude: position.lat(),
                        longitude: position.lng(),
                        csrfmiddlewaretoken: getCsrfToken() // Function to get CSRF token
                    },
                    success: function(response) {
                        // Handle success
                        console.log("Widget saved successfully.");
                    },
                    error: function(error) {
                        // Handle error
                        console.error("Error saving widget:", error);
                    }
                });
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    });

    // Event listener for calculating and displaying route
    calculateDistanceButton.addEventListener("click", function () {
        const userAddress = userAddressInput.value;
        if (userAddress) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    calculateAndDisplayRoute(userLocation, userAddress);
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        } else {
            alert("Please enter your address.");
        }
    });

    // Function to calculate and display route
    function calculateAndDisplayRoute(userLocation, destinationAddress) {
        directionsService.route({
            origin: userLocation,
            destination: destinationAddress,
            travelMode: 'DRIVING',
        }, function (response, status) {
            if (status === 'OK') {
                directionsRenderer.setDirections(response);
            } else {
                alert('Error calculating route: ' + status);
            }
        });
    }
});
