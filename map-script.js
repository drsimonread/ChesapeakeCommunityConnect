document.addEventListener("DOMContentLoaded", function () {
    let map;
    const addMarkerButton = document.getElementById("add-marker-button");
    const addMarkerForm = document.getElementById("add-marker-form");
    const userMarkerForm = document.getElementById("marker-form");

    function initMap() {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
            zoom: 8,
        });
    }

    addMarkerButton.addEventListener("click", () => {
        addMarkerForm.style.display = "block";
    });

    userMarkerForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const address = document.getElementById("address").value;
        const city = document.getElementById("city").value;
        const state = document.getElementById("state").value;
        const zip = document.getElementById("zip").value;
        const fullAddress = `${address}, ${city}, ${state} ${zip}`;

        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ address: fullAddress }, function (results, status) {
            if (status === 'OK') {
                const position = results[0].geometry.location;
                const marker = new google.maps.Marker({
                    position,
                    map,
                    title: title,
                });

                const infowindow = new google.maps.InfoWindow({
                    content: `<h3>${title}</h3><p>${description}</p>`
                });

                marker.addListener('click', function () {
                    infowindow.open(map, marker);
                });

                map.setCenter(position);
                addMarkerForm.style.display = "none";
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    });

    google.maps.event.addDomListener(window, 'load', initMap);
});
