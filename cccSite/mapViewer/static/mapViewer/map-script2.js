let map;
let autocomplete;
const posts = JSON.parse(JSON.parse(
    document.currentScript.nextElementSibling.textContent
    ));//*/
const markerList = [];
const infoWindowList = [];
function initMap() {
    console.log(posts)
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_location'),
        {fields : ["address_components"],
        }
    );
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
    });
    for(let item of posts){
        console.log(item)
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

