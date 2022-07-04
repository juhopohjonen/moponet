// fetch meets

// create req object + add headers + send
var meetRequest = new XMLHttpRequest();
meetRequest.open('POST', fetchUrl);

meetRequest.setRequestHeader('X-CSRFToken', csrf_token);
meetRequest.send();

const clickThisText = 'Klikkaa lisätietoja varten';

var meets = null;
const today = new Date();

// handle loading
meetRequest.onload = function () {
    if (meetRequest.status != 200) {
        alert('Virhe palvelinpyynnössä.');
        return;
    }

    meets = JSON.parse(meetRequest.responseText)['meets']; 
    
    for (var i = 0; i < meets.length; i++) {
        let meet = meets[i];

        // real meet month = meet_month - 1 because js months start from 0
        let meet_date = new Date(meet['meet_year'], meet['meet_month'] - 1, meet['meet_day'], 0, 0, 0, 0);
        console.log('date', meet_date);

        // add only meets in future
        if (meet_date > today) {
            addMeetToMap(meet);
        }


    }
}

function addMeetToMap (meet) {
    // convert str to float
    let lat = parseFloat(meet['latitudes']);
    let lon = parseFloat(meet['longitudes']);

    let marker = addMarkerToMap(lat, lon);


    // create popup and bind it to the marker
    let popupContent = document.createElement('div');
    let link = popupContent.appendChild(document.createElement('a'));
    
    link.href = viewurl + "?meet=" + meet['id'];

    let text = link.appendChild(document.createElement('h5')).append(meet['meet_name']);
    

    marker.bindPopup(popupContent);
}