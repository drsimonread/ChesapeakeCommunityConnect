let map; //map object
let autocomplete; //autocomplete object
const posts = JSON.parse(JSON.parse(document.currentScript.nextElementSibling.textContent));
const markerList = []; //use this to iteratively create post markers on the map
const infoWindowList = []; //same but for the post windows for when you click on the markers
let directionsService;
let directionsRenderer;

async function initMap() {
    autocomplete = new google.maps.places.Autocomplete(document.getElementById('id_location'), {
        fields: ["address_components"],
    });
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
        mapId: 'DEMO_MAP_ID'
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    for (let item of posts) {
        const title = item.fields.title;
        const description = item.fields.description;
        const position = { lat: item.fields.geoCode.geometry.location.lat, lng: item.fields.geoCode.geometry.location.lng };
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

        const marker = new AdvancedMarkerElement({
            position,
            map,
            title: title,
        });
        const infowindow = new google.maps.InfoWindow({
            content: `<h3>${title}</h3><p>${description}</p>`
        });

        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markerList.push(marker);
        infoWindowList.push(infowindow);
    }
}

function calculateRoute(origin, destination) {
    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: 'DRIVING',
    }, function(response, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(response);
            const route = response.routes[0];
            const distance = route.legs[0].distance.text;
            const duration = route.legs[0].duration.text;
            alert(`Distance: ${distance}, Estimated travel time: ${duration}`);
        } else {
            alert('Directions request failed due to ' + status);
        }
    });
}

function getUserLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            callback(userLocation);
        }, function() {
            // User denied geolocation prompt or it failed; ask for a manual input
            const manualLocation = prompt("Geolocation is not available. Please enter your location manually:");
            geocodeAddress(manualLocation, callback);
        });
    } else {
        // Geolocation is not supported; ask for a manual input
        const manualLocation = prompt("Geolocation is not supported by this browser. Please enter your location manually:");
        geocodeAddress(manualLocation, callback);
    }
}

function geocodeAddress(address, callback) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': address }, function(results, status) {
        if (status === 'OK') {
            callback(results[0].geometry.location);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    initMap();

    const calculateDistanceButton = document.getElementById("calculate-distance");
    const userAddressInput = document.getElementById("user-address");

    calculateDistanceButton.addEventListener("click", function() {
        const userAddress = userAddressInput.value;
        if (userAddress) {
            getUserLocation(function(userLocation) {
                calculateRoute(userLocation, userAddress);
            });
        } else {
            alert("Please enter your address.");
        }
    });
});
