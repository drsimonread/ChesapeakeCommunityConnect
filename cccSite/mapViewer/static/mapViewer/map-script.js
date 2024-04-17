// JavaScript for slideshow functionality
let map;
const posts = JSON.parse(JSON.parse(document.currentScript.nextElementSibling.textContent)); //don't know why it needs to JSON.parse twice, but with only one posts is a String
const markerList = []; //use this to iteratively create post markers on the map
const infoWindowList = []; //same but for the post windows for when you click on the markers
async function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
        mapId: '946a9c10600de2ba'
    });

    for (let item of posts) {
        const title = item.fields.title;
        const description = item.fields.description;
        const stringArray = window.location.href.split("?")
        const postURL = stringArray[0] + "post/" + item.pk;
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
                <a href="${postURL}">See More</a>
            `
        });
        
        marker.addListener('click', function() {
            for (let item of infoWindowList){
                item.close();
            }
            infowindow.open(map, marker);
        });

        markerList.push(marker);
        infoWindowList.push(infowindow);
    }
}