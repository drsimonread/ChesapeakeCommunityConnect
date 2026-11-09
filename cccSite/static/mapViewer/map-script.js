let map;
let markerLayer;
const mapData = JSON.parse(document.getElementById("map-data").textContent);
const forums = typeof mapData === "string" ? JSON.parse(mapData) : mapData;

function showMapError(message) {
    const status = document.getElementById("map-status");
    if (status) {
        status.hidden = false;
        status.textContent = message;
    }
}

function getPosition(item) {
    const location = item.fields.geoCode?.geometry?.location || item.fields.geoCode;
    if (!location || typeof location.lat !== "number" || typeof location.lng !== "number") {
        return null;
    }
    return [location.lat, location.lng];
}

function renderMarkers() {
    markerLayer.clearLayers();
    for (const item of forums) {
        const position = getPosition(item);
        if (!position) continue;

        const title = item.fields.title;
        const description = item.fields.description;
        const forumURL = `${window.location.origin}${window.location.pathname}post/${item.pk}`;
        L.marker(position)
            .bindPopup(`<h3>${title}</h3><p>${description}</p><a href="${forumURL}">See More</a>`)
            .addTo(markerLayer);
    }
}

function initMap() {
    if (!window.L) {
        showMapError("The map library could not be loaded. Please check your internet connection.");
        return;
    }

    map = L.map("map").setView([38.9, -77.0], 8);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    markerLayer = L.layerGroup().addTo(map);
    renderMarkers();
}

async function createPost() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const address = document.getElementById("address").value;
    const city = document.getElementById("city").value;
    const state = document.getElementById("state").value;
    const zipcode = document.getElementById("zipcode").value;

    if (!address) {
        alert("Please enter an address");
        return;
    }

    const query = encodeURIComponent(`${address}, ${city}, ${state} ${zipcode}`);
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&q=${query}`, {
        headers: { Accept: "application/json" }
    });
    const results = await response.json();
    if (!results.length) {
        alert("Address not found");
        return;
    }

    const location = [Number(results[0].lat), Number(results[0].lon)];
    const marker = L.marker(location)
        .bindPopup(`<h4>${title}</h4><p>${description}</p><p>${address}, ${city}, ${state} ${zipcode}</p>`)
        .addTo(markerLayer);
    marker.openPopup();
    map.setView(location, 14);
}

document.addEventListener("DOMContentLoaded", () => {
    window.createPost = createPost;
    initMap();
});
