let map;
const mapData = JSON.parse(document.getElementById("map-data").textContent);
const forums = typeof mapData === "string" ? JSON.parse(mapData) : mapData;
const infoWindowList = [];
const markerList = [];
let AdvancedMarkerElementClass;
let locationGroups = new Map();
const SPLIT_MARKERS_ZOOM = 14;

function getPosition(item) {
    const geoCode = item.fields.geoCode;
    const location =
        geoCode?.geometry?.location ||
        geoCode?.location ||
        geoCode;

    if (!location ||
        (typeof location.lat !== "number" && typeof location.lat !== "string") ||
        (typeof location.lng !== "number" && typeof location.lng !== "string")) {
        return null;
    }

    const lat = Number(location.lat);
    const lng = Number(location.lng);
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
        return null;
    }

    return { lat, lng };
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function showMapError(message) {
    const status = document.getElementById("map-status");
    if (status) {
        status.hidden = false;
        status.textContent = message;
    }
}

function closeInfoWindows() {
    for (const openWindow of infoWindowList) {
        openWindow.close();
    }
}

function openPostListMarker(group) {
    const postCount = group.posts.length;
    const markerContent = document.createElement("div");
    markerContent.style.cssText =
        "display:flex;align-items:center;justify-content:center;" +
        "min-width:32px;height:32px;padding:0 6px;box-sizing:border-box;" +
        "border:3px solid #fff;border-radius:18px;background:#b42318;" +
        "color:#fff;font:700 14px Arial,sans-serif;" +
        "box-shadow:0 2px 7px rgba(0,0,0,.45);";
    markerContent.textContent = String(postCount);
    markerContent.setAttribute("aria-label", `${postCount} posts at this location`);

    const marker = new AdvancedMarkerElementClass({
        position: group.position,
        map,
        title: `${postCount} posts at this location`,
        content: markerContent,
    });

    let content = `<h3>${postCount} posts at this location</h3><div>`;
    for (const item of group.posts) {
        const title = escapeHtml(item.fields.title);
        const description = escapeHtml(item.fields.description);
        const forumURL = `${window.location.origin}${window.location.pathname}post/${item.pk}`;
        content += `
            <div style="margin-bottom:10px;">
                <h4 style="margin:0 0 4px;"><a href="${forumURL}">${title}</a></h4>
                <p style="margin:0;">${description}</p>
            </div>
        `;
    }
    content += "</div>";

    const infowindow = new google.maps.InfoWindow({ content });
    marker.addListener("click", function() {
        closeInfoWindows();
        infowindow.open(map, marker);
    });

    markerList.push(marker);
    infoWindowList.push(infowindow);
}

function openIndividualMarker(item, position) {
    const title = escapeHtml(item.fields.title);
    const description = escapeHtml(item.fields.description);
    const forumURL = `${window.location.origin}${window.location.pathname}post/${item.pk}`;
    const markerContent = document.createElement("div");
    markerContent.style.cssText =
        "width:24px;height:24px;border:3px solid #fff;border-radius:50% 50% 50% 0;" +
        "background:#1d4ed8;transform:rotate(-45deg);" +
        "box-shadow:0 2px 7px rgba(0,0,0,.45);";

    const marker = new AdvancedMarkerElementClass({
        position,
        map,
        title: item.fields.title,
        content: markerContent,
    });
    const infowindow = new google.maps.InfoWindow({
        content: `
            <h3>${title}</h3>
            <p>${description}</p>
            <a href="${forumURL}">See More</a>
        `
    });

    marker.addListener("click", function() {
        closeInfoWindows();
        infowindow.open(map, marker);
    });

    markerList.push(marker);
    infoWindowList.push(infowindow);
}

function renderMarkers() {
    for (const marker of markerList) {
        marker.map = null;
    }
    markerList.length = 0;
    closeInfoWindows();

    if (map.getZoom() >= SPLIT_MARKERS_ZOOM) {
        for (const group of locationGroups.values()) {
            if (group.posts.length === 1) {
                openIndividualMarker(group.posts[0], group.position);
                continue;
            }

            group.posts.forEach((item, index) => {
                const ring = Math.floor(index / 8);
                const angleIndex = index % 8;
                const angle = (angleIndex * 45 * Math.PI) / 180;
                const distance = 0.00045 * (ring + 1);
                const position = {
                    lat: group.position.lat + Math.sin(angle) * distance,
                    lng: group.position.lng + Math.cos(angle) * distance,
                };
                openIndividualMarker(item, position);
            });
        }
    } else {
        for (const group of locationGroups.values()) {
            if (group.posts.length === 1) {
                openIndividualMarker(group.posts[0], group.position);
            } else {
                openPostListMarker(group);
            }
        }
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
        AdvancedMarkerElementClass = AdvancedMarkerElement;
        locationGroups = new Map();

        for (const item of forums) {
            const position = getPosition(item);
            if (!position) continue;

            const locationKey = `${position.lat},${position.lng}`;
            if (!locationGroups.has(locationKey)) {
                locationGroups.set(locationKey, { position, posts: [] });
            }
            locationGroups.get(locationKey).posts.push(item);
        }

        renderMarkers();
        map.addListener("zoom_changed", renderMarkers);
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
