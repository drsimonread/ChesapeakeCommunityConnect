let map;
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
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
        for (let item of forums) {
            const title = item.fields.title;
            const description = item.fields.description;
            const forumURL = `${window.location.origin}${window.location.pathname}post/${item.pk}`;
            const position = { lat: item.fields.geoCode.geometry.location.lat, lng: item.fields.geoCode.geometry.location.lng };
            const infoContent = document.createElement("div");
            const heading = document.createElement("h3");
            const summary = document.createElement("p");
            const link = document.createElement("a");
            heading.textContent = title;
            summary.textContent = description;
            link.href = forumURL;
            link.textContent = "See More";
            infoContent.append(heading, summary, link);

            const marker = new AdvancedMarkerElement({
                position,
                map,
                title: title,
            });
            const infowindow = new google.maps.InfoWindow({
                content: infoContent
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


document.addEventListener("DOMContentLoaded", function () {
    const choice = document.getElementById("post-access-choice");
    const guestForm = document.getElementById("post-form");
    const guestChoiceForm = document.getElementById("guest-choice-form");
    const changeMethod = document.getElementById("back-to-post-choice");

    guestChoiceForm?.addEventListener("submit", (event) => {
        event.preventDefault();
        choice.hidden = true;
        guestForm.hidden = false;
        document.getElementById("email").focus();
    });

    changeMethod?.addEventListener("click", (event) => {
        event.preventDefault();
        guestForm.hidden = true;
        choice.hidden = false;
        document.getElementById("continue-as-guest").focus();
    });

    if (!guestForm.hidden) {
        document.getElementById("email").focus();
    }
});