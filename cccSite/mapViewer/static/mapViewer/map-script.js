document.addEventListener("DOMContentLoaded", function () {
    let map;
    let directionsService;
    let directionsRenderer;

    function initMap() {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 38.9, lng: -77.0 },
            zoom: 8,
        });

        directionsService = new google.maps.DirectionsService();
        directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(map);
    }

    initMap();

    const addMarkerButton = document.getElementById("add-marker-button");
    const addMarkerForm = document.getElementById("add-marker-form");
    const userMarkerForm = document.getElementById("marker-form");
    const calculateDistanceButton = document.getElementById("calculate-distance");
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

    addMarkerButton.addEventListener("click", () => {
        addMarkerForm.style.display = "block";
    });

    userMarkerForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(userMarkerForm);
        const fullAddress = `${formData.get("address")}, ${formData.get("city")}, ${formData.get("state")} ${formData.get("zip")}`;

        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ address: fullAddress }, function (results, status) {
            if (status === 'OK') {
                const position = results[0].geometry.location;
                new google.maps.Marker({
                    position,
                    map,
                    title: formData.get("title"),
                });

                map.setCenter(position);
                addMarkerForm.style.display = "none";

                // AJAX call to send data to Django backend
                $.ajax({
                    type: "POST",
                    url: "/save_widget/",
                    data: {
                        title: formData.get("title"),
                        description: formData.get("description"),
                        latitude: position.lat(),
                        longitude: position.lng(),
                        csrfmiddlewaretoken: getCsrfToken()
                    },
                    success: function(response) {
                        console.log("Widget saved successfully.");
                    },
                    error: function(error) {
                        console.error("Error saving widget:", error);
                    }
                });
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    });

    calculateDistanceButton.addEventListener("click", function () {
        const userAddress = userAddressInput.value.trim();
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
