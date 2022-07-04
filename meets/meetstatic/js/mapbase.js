var map = L.map('map').setView([65.5, 28], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

function addMarkerToMap(lat, lon) {
    var marker = L.marker([lat, lon])
    marker.addTo(map);

    return marker;
}
