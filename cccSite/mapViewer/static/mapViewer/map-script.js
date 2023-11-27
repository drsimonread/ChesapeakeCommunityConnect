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

                // AJAX call to send data to Django backend
                $.ajax({
                    type: "POST",
                    url: "/save_widget/", // URL of the Django view
                    data: {
                        title: title,
                        description: description,
                        latitude: position.lat(),
                        longitude: position.lng(),
                        csrfmiddlewaretoken: getCsrfToken() // Function to get CSRF token
                    },
                    success: function(response) {
                        // Handle success
                        console.log("Widget saved successfully.");
                    },
                    error: function(error) {
                        // Handle error
                        console.error("Error saving widget:", error);
                    }
                });
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    });

    function getCsrfToken() {
        // Function to get CSRF token from cookie
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    google.maps.event.addDomListener(window, 'load', initMap);
});
