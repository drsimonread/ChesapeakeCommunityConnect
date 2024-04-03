// JavaScript for slideshow functionality
let slideIndex = 0;
showSlides();

function showSlides(n) {
    let i;
    const slides = document.getElementsByClassName("mySlides");
    if (n != undefined) {
        slideIndex = n; // Set slideIndex to the specified value if provided
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    if (slideIndex >= slides.length) {slideIndex = 0} // Reset index if it exceeds the number of slides
    if (slideIndex < 0) {slideIndex = slides.length - 1} // Wrap around to the last slide if index is negative
    slides[slideIndex].style.display = "block";
    slideIndex++;
    setTimeout(showSlides, 2000); // Change image every 2 seconds
}

function plusSlides(n) {
    showSlides(slideIndex += n);
}


async function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
        mapId: '946a9c10600de2ba'
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    for (let item of posts) {
        const title = item.fields.title;
        const description = item.fields.description;
        const postID = item.pk; // Get the post ID
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
                <a href="#" onclick="openSlideshow(${postID})">See More</a> <!-- Call openSlideshow function -->
            `
        });
        
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markerList.push(marker);
        infoWindowList.push(infowindow);
    }
}

// Function to open the slideshow popup
function openSlideshow(postID) {
    window.location.href = `/slideshow/${postID}/`;
}