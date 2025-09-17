let map; //map object
const posts = JSON.parse(JSON.parse(document.currentScript.nextElementSibling.textContent));
const markerList = []; //use this to iteratively create post markers on the map
const infoWindowList = []; //same but for the post windows for when you click on the markers

async function initMap() {

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
        const postURL = window.location.href + "post/" + item.pk;
        const position = { lat: item.fields.geoCode.geometry.location.lat, lng: item.fields.geoCode.geometry.location.lng };
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
                <img src="${item.fields.media_file.url}" alt="Media" /> <!-- Assuming the media file is an image -->
                <a href="${postURL}">See More</a>
            `
        });
        
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markerList.push(marker);
        infoWindowList.push(infowindow);
    }
}
