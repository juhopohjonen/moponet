var createXHR = new XMLHttpRequest();

// get input fields from the DOM
const meetName = document.getElementById('name');
const description = document.getElementById('description');
const date = document.getElementById('date');

// set meet coordinate values, defaults to null
var meetLat = null;
var meetLon = null;

var markers = [];

var nocoordsError = document.getElementById('nocoords');


function createmeet() {
    createXHR.open('POST', createUrl);
    createXHR.setRequestHeader('X-CSRFToken', csrf_token);
    createXHR.setRequestHeader("Content-Type", "application/json; charset=utf8");


    // remove all existing alerts
    for (var i = 0; i < document.getElementsByClassName('alert').length; i++) {
        document.getElementsByClassName('alert')[i].style.display = 'none';
    }

    if (meetLat == null | meetLon == null) {
        nocoordsError.style.display = 'block';
        return;
    }

    // wrap lat and lon into a json
    var base = JSON.parse('{}');

    base['lat'] = meetLat;
    base['lon'] = meetLon;
    
    base['name'] = meetName.value;
    base['description'] = description.value;
    base['date'] = date.value;

    createXHR.send(JSON.stringify(base));
}


function setMeetLocation(e) {

    // remove all existing markers
    for (var i = 0; i < markers.length; i++) {
        markers[i].remove();
    }

    markers.length = 0;


    var latlng = e['latlng'];

    meetLat = latlng['lat'];
    meetLon = latlng['lng'];
  
    var marker = addMarkerToMap(meetLat, meetLon);
    markers.push(marker);
} 

map.on('click', setMeetLocation); 

createXHR.onload = function () {
    var response = JSON.parse(createXHR.responseText);
    if (response['isRedirect'] == true) {
        window.location.replace(response['redirecturl']);
    }
    
}