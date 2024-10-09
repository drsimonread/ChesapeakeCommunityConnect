var slideIndex = 1;
let map;
const locCode = JSON.parse(document.currentScript.nextElementSibling.textContent);
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {slideIndex = 1;}
    if (n < 1) {slideIndex = slides.length;}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
}

async function initMap(){
    const address = locCode.formatted_address;
    const position = { lat: locCode.geometry.location.lat, lng: locCode.geometry.location.lng };
    map = new google.maps.Map(document.getElementById("map"), {
        center: position, // Chesapeake Bay Area
        zoom: 12,
        mapId: '946a9c10600de2ba'
    });


    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const marker = new AdvancedMarkerElement({
        position,
        map,
    });
    const infowindow = new google.maps.InfoWindow({
        content: `
            <h3>${address}</h3>
        `
    });
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
    
}