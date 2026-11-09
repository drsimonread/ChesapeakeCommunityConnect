let map;
let geocoder;
const mapData = JSON.parse(document.getElementById("map-data").textContent);
const forums = typeof mapData === "string" ? JSON.parse(mapData) : mapData;
const infoWindowList = [];

function showMapError(message) {
    const status = document.getElementById("map-status");
    if (status) {
        status.hidden = false;
        status.textContent = message;
    }
}

async function initMap() {
    try {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
            zoom: 8,
            mapId: '946a9c10600de2ba'
        });
        geocoder = new google.maps.Geocoder();

        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
        for (let item of forums) {
            const title = item.fields.title;
            const description = item.fields.description;
            const forumURL = `${window.location.origin}${window.location.pathname}post/${item.pk}`;
            const position = { lat: item.fields.geoCode.geometry.location.lat, lng: item.fields.geoCode.geometry.location.lng };

            const marker = new AdvancedMarkerElement({
                position,
                map,
                title: title,
            });
            const infowindow = new google.maps.InfoWindow({
                content: `
                    <h3>${title}</h3>
                    <p>${description}</p>
                    <a href="${forumURL}">See More</a>
                `
            });

            marker.addListener('click', function() {
                for (let item of infoWindowList){
                    item.close();
                }
                infowindow.open(map, marker);
            });

            infoWindowList.push(infowindow);
        }
        const addressInput = document.getElementById("address");

        if (addressInput) {

            const autocomplete = new google.maps.places.Autocomplete(addressInput, {
                types: ["address"],
                componentRestrictions: { country: "us" }
            });

            autocomplete.addListener("place_changed", () => {

                const place = autocomplete.getPlace();

                if (!place.geometry) return;

                for (const component of place.address_components) {

                    const types = component.types;

                    if (types.includes("locality")) {
                        document.getElementById("city").value = component.long_name;
                    }

                    if (types.includes("administrative_area_level_1")) {
                        document.getElementById("state").value = component.short_name;
                    }

                    if (types.includes("postal_code")) {
                        document.getElementById("zipcode").value = component.long_name;
                    }
                }
            });
        }
    } catch (error) {
        console.error("Unable to initialize Google Maps.", error);
        showMapError("The map could not be loaded. Please verify the Google Maps API key and website restrictions.");
    }
}

window.gm_authFailure = function() {
    showMapError("The map could not be loaded because this website is not authorized to use the Google Maps API key.");
};


function createPost() {

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const address = document.getElementById("address").value;
    const city = document.getElementById("city").value;
    const state = document.getElementById("state").value;
    const zipcode = document.getElementById("zipcode").value;

    const fullAddress = `${address}, ${city}, ${state} ${zipcode}`;

    if (!address) {
        alert("Please enter an address");
        return;
    }

    geocoder.geocode({ address: fullAddress }, function(results, status) {

        if (status === "OK") {

            const location = results[0].geometry.location;

            const marker = new google.maps.Marker({
                map: map,
                position: location,
                title: title
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <h4>${title}</h4>
                    <p>${description}</p>
                    <p>${fullAddress}</p>
                `
            });

            marker.addListener("click", () => {
                infoWindow.open(map, marker);
            });

            map.setCenter(location);
            map.setZoom(14);

        } else {
            alert("Address not found: " + status);
        }

    });
}
document.addEventListener("DOMContentLoaded", function () {
    window.createPost = createPost;

});