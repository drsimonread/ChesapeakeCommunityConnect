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
            // Your existing code for handling the marker form submission
        });
    
        // Enhanced event listener for calculating and displaying route
        calculateDistanceButton.addEventListener("click", function (e) {
            e.preventDefault(); // Prevent form submission or any default action
            toggleAddressInputVisibility(); // Call to toggle the visibility of address input
    
            const userAddress = userAddressInput.value;
            if (userAddress) {
                calculateRouteUsingGeolocation(userAddress);
            } else {
                alert("Please enter your address.");
            }
        });
    
        function toggleAddressInputVisibility() {
            var addressInput = document.getElementById('user-address');
            addressInput.style.display = (addressInput.style.display === 'none' || addressInput.style.display === '') ? 'block' : 'none';
        }
    
        function calculateRouteUsingGeolocation(destinationAddress) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    calculateAndDisplayRoute(userLocation, destinationAddress);
                }, function (error) {
                    alert("Error getting user location: " + error.message);
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
    
        function calculateAndDisplayRoute(origin, destination) {
            directionsService.route({
                origin: origin,
                destination: destination,
                travelMode: 'DRIVING',
            }, function (response, status) {
                if (status === 'OK') {
                    directionsRenderer.setDirections(response);
                } else {
                    alert('Directions request failed due to ' + status);
                }
            });
        }
    });
    
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
