

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

    }

    initMap(); // Call the initMap function when the DOM is loaded
    
    // Add event listeners and other functionalities here
});


    addMarkerButton.addEventListener("click", () => {
        addMarkerForm.style.display = "block";
    });

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

    //respond to a request to search -- currently broken
    searchForm.addEventListener("submit", function (event){
        event.preventDefault();
        const searchText = document.getElementById("search-text");
        $.ajax({
            type:"GET",
            url:"/mapSearch/", 
            data: {
                searchText: searchText,
                csrfmiddlewaretoken: getCsrfToken()
            },
            success: function(response) {
                console.log("Searched successfully.");

            },
            error: function(error) {
                console.error("error searching: ", error);
            }
        });
    });

    searchForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const searchText = document.getElementById("search-text").value;
        $.ajax({
            type: "GET",
            url: "/search_widgets/",
            data: { searchText: searchText },
            success: function (response) {
                // Clear existing markers
                // Loop through response.widgets to add new markers
                console.log("Search results:", response.widgets);
            },
            error: function (error) {
                console.error("Error searching: ", error);
            }
        });
    });

    function getCsrfToken() {
        // Function to get CSRF token from cookie
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

    google.maps.event.addDomListener(window, 'load', initMap);

    document.addEventListener("DOMContentLoaded", function () {
        let map;
        const addMarkerButton = document.getElementById("add-marker-button");
        const addMarkerForm = document.getElementById("add-marker-form");
        const userMarkerForm = document.getElementById("marker-form");
        const calculateDistanceButton = document.getElementById("calculate-distance");
        const useCurrentLocationButton = document.getElementById("use-current-location");
        const userAddressInput = document.getElementById("user-address");
        const distanceResultDiv = document.getElementById("distance-result");
        const downloadMapButton = document.getElementById("download-map");
    
        function initMap() {
            map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
                zoom: 8,
            });
            directionsMap = new google.maps.Map(document.getElementById("directionsMap"), {
                center: { lat: 38.9, lng: -77.0 }, // Example center
                zoom: 8,
            });
        
            directionsService = new google.maps.DirectionsService();
            directionsRenderer = new google.maps.DirectionsRenderer();
            directionsRenderer.setMap(directionsMap);
        }

        function calculateAndDisplayRoute(directionsService, directionsRenderer, start, end) {
            directionsService.route(
                {
                    origin: start,
                    destination: end,
                    travelMode: 'DRIVING',
                },
                (response, status) => {
                    if (status === 'OK') {
                        directionsRenderer.setDirections(response);
                    } else {
                        window.alert('Directions request failed due to ' + status);
                    }
                }
            );
        }
    
        useCurrentLocationButton.addEventListener("click", function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    const userLocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    calculateDistance(userLocation, "Widget Location Here"); // Replace "Widget Location Here" with actual widget location
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        });
    
        calculateDistanceButton.addEventListener("click", function () {
            const userAddress = userAddressInput.value;
            if (userAddress) {
                calculateDistance(userAddress, "Widget Location Here"); // Replace "Widget Location Here" with actual widget location
            } else {
                alert("Please enter your address or use current location.");
            }
        });
    
        // Download Map functionality
        // Note: Direct downloading of Google Maps as images is restricted; consider using a screen capture tool or API for map snapshots.
        downloadMapButton.addEventListener("click", function () {
            alert("Downloading of the map directly is not supported by Google Maps. Please use a screen capture tool.");
        });
    
        google.maps.event.addDomListener(window, 'load', initMap);
    });

    // Add event listeners to markers for selection
for (let i = 0; i < markerList.length; i++) {
    markerList[i].addListener('click', function () {
        const markerPosition = markerList[i].getPosition();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                const confirmDirections = confirm("Would you like directions from your current location?");
                if (confirmDirections) {
                    calculateAndDisplayRoute(userLocation, markerPosition);
                } else {
                    const userAddress = prompt("Please enter your address:");
                    if (userAddress) {
                        // Use Geocoding API to convert userAddress to LatLng
                        const geocoder = new google.maps.Geocoder();
                        geocoder.geocode({ 'address': userAddress }, function (results, status) {
                            if (status === 'OK') {
                                const userLocation = results[0].geometry.location;
                                calculateAndDisplayRoute(userLocation, markerPosition);
                            } else {
                                alert('Geocode was not successful for the following reason: ' + status);
                            }
                        });
                    }
                }
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });
}
    