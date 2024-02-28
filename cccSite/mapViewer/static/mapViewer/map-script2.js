let map; //map object
let autocomplete;//autocomplete object
const posts = JSON.parse(JSON.parse(
    document.currentScript.nextElementSibling.textContent
    ));//don't know why it needs to JSON.parse twice, but with only one posts is a String
const markerList = []; //use this to iteratively create post markers on the map
const infoWindowList = []; //same but for the post windows for when you click on the markers
async function initMap() { //this function is called by the API script initalization in the HTML due to the callback= argument in the src url
    //console.log("hi")
    autocomplete = new google.maps.places.Autocomplete( //adds an autocompleter to the address field of the create post form
        document.getElementById('id_location'),
        {fields : ["address_components"],
        }
    );
    map = new google.maps.Map(document.getElementById("map"), { //adds the map to the map element
        center: { lat: 38.9, lng: -77.0 }, // Chesapeake Bay Area
        zoom: 8,
        mapId: 'DEMO_MAP_ID'
    });
    for(let item of posts){ //for each post that has been provided to the template
        //console.log("test")
        const title = item.fields.title;
        const description = item.fields.description;
        const position = { lat : item.fields.geoCode.geometry.location.lat, lng : item.fields.geoCode.geometry.location.lng }; //get info
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

        const marker = new AdvancedMarkerElement({//create a marker on the map
            position,
            map,
            title: title,
        });
        const infowindow = new google.maps.InfoWindow({//create an info window for the current marker
            content: `<h3>${title}</h3><p>${description}</p>`
        });

        marker.addListener('click', function () {
            infowindow.open(map, marker);//associate the marker and info window with the onclick
        });

        markerList.push(marker);//add marker to the markerList
        infoWindowList.push(infowindow);//add infowindo to the infoWindowList

        }
    }

