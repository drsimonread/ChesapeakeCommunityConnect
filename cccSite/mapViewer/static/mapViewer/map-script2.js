let map; //map object
const posts = JSON.parse(JSON.parse(document.currentScript.nextElementSibling.textContent));
const markerList = []; //use this to iteratively create post markers on the map
const infoWindowList = []; //same but for the post windows for when you click on the markers


// Group tags dynamically
function extractUniqueTags(posts) {
    const tagSet = new Set();
    posts.forEach(post => {
        post.fields.tags.forEach(tag => tagSet.add(tag));
    });
    return Array.from(tagSet);
}

function populateTags(tags) {
    const select = document.getElementById("tag-filter");
    if (!select) return;
    select.innerHTML = `<option value="All">All Categories</option>`;
    tags.forEach(tag => {
        const option = document.createElement("option");
        option.value = tag;
        option.textContent = tag;
        select.appendChild(option);
    });
}

async function renderMarkers(filteredTag = "All") {
    // Clear old markers
    markerList.forEach(marker => marker.setMap(null));
    markerList.length = 0;
    infoWindowList.length = 0;

    const projectList = document.getElementById("project-list");
    if (projectList) projectList.innerHTML = "";

    for (let item of posts) {
        const title = item.fields.title;
        const description = item.fields.description;
        const tags = item.fields.tags;
        const postURL = window.location.href + "post/" + item.pk;
        const position = {
            lat: item.fields.geoCode.geometry.location.lat,
            lng: item.fields.geoCode.geometry.location.lng
        };

        if (filteredTag !== "All" && !tags.includes(filteredTag)) continue;

        // Add to project list
        const li = document.createElement("li");
        li.textContent = title;
        if (projectList) projectList.appendChild(li);

        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

        const marker = new AdvancedMarkerElement({
            position,
            map,
            title: title,
        });

        const infowindow = new google.maps.InfoWindow({
            content: `
                <h3>${title}</h3>
                <p>${description}</p>
                <img src="${item.fields.media_file?.url || ''}" alt="Media" />
                <a href="${postURL}">See More</a>
            `
        });

        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });

        markerList.push(marker);
        infoWindowList.push(infowindow);
    }
}


async function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
        mapId: 'DEMO_MAP_ID'
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    const uniqueTags = extractUniqueTags(posts);
    populateTags(uniqueTags);
    await renderMarkers(); 

}

document.addEventListener("DOMContentLoaded", () => {
    const filterSelect = document.getElementById("tag-filter");
    if (filterSelect) {
        filterSelect.addEventListener("change", async (e) => {
            await renderMarkers(e.target.value);
        });
    }
});
