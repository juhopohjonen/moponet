// get ui elements from the DOM

const participateBtns = document.getElementById('participate');
const leaveBtns = document.getElementById('leave');
const loadingWheel = document.getElementById('loading');

// load participation status (has user participated)

var loadParticipation = new XMLHttpRequest();

var loadParticipationUrl = participateUrl + "?type=getparticipation&meetid=" + meetid;
var changeParticipateUrl = participateUrl + "?type=change&meetid=" + meetid;

// open request + add X-CSRFToken
loadParticipation.open('POST', loadParticipationUrl);
loadParticipation.setRequestHeader('X-CSRFToken', csrf_token);


loadParticipation.send();

loadParticipation.onload = function () {
    // handle errors

    if (loadParticipation.readyState == 4 && loadParticipation.status == 200) {
    
        loadingWheel.style.display = 'none';        
        
        var response = JSON.parse(loadParticipation.responseText);
        hasParticipated = response['hasParticipated'];

        // change ui
        changeParticipationUI(!hasParticipated);

    } else {
        alert('Virhe palvelinyhteyksissä.');
        loadingWheel.style.display = 'none';
    }
}

function changeParticipationUI (showParticipate) {

    if (showParticipate) {
        participateBtns.style.display = 'block';
        leaveBtns.style.display = 'none';
    } else {
        participateBtns.style.display = 'none';
        leaveBtns.style.display = 'block';
    }
}


// function for sending xhr to server to participate
function changeParticipation (participate) {
    var changeParticipationXHR = new XMLHttpRequest();
    changeParticipationXHR.open('POST', changeParticipateUrl);

    var content = JSON.parse('{}');
    content['wantsToParticipate'] = participate;

    changeParticipationXHR.setRequestHeader('X-CSRFToken', csrf_token);
    changeParticipationXHR.setRequestHeader("Content-Type", "application/json; charset=utf8");

    changeParticipationXHR.send(JSON.stringify(content));

    // change ui

    changeParticipationUI(!participate);
}