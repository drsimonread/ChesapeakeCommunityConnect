document.addEventListener("DOMContentLoaded", function () {
    let map;
    const posts = JSON.parse(
        document.currentScript.nextElementSibling.textContent
      );//*/
    console.log(posts)
    const markerList = [];
    const infoWindowList = [];
    function initMap() {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
            zoom: 8,
        });
        for(let item of posts){
            const title = item.fields.title;
            const description = item.fields.description;
            const position = {lat : item.fields.latitude, lng : item.fields.longitude};
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

            markerList.push(marker);
            infoWindowList.push(infowindow);

        }//*/
    }

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
