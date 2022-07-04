// make post request to followpoint


var followSpinner = document.getElementById('followSpin');

var followBtn = document.getElementById('followBtn');
var unfollowBtn = document.getElementById('unfollowBtn');

var ownerMsg = document.getElementById('ownerMsg');


var followStatusXHR = new XMLHttpRequest();
var followStatusUrl = followpoint + "?type=status";

var setFollowXHR = new XMLHttpRequest();
var setFollowUrl = followpoint + "?type=set"


function getFollowStatus()
{
    followStatusXHR.open('POST', followStatusUrl);
    followStatusXHR.setRequestHeader('X-CSRFToken', csrf_token);

    var data = JSON.parse('{}');
    data['target_user_id'] = current_user_id;

    followStatusXHR.setRequestHeader("Content-Type", "application/json");

    followStatusXHR.send(JSON.stringify(data));
}

function setFollow (isFollowRequest) {
    //  user has not followed => make follow request

    setFollowXHR.open('POST', setFollowUrl);
    setFollowXHR.setRequestHeader('X-CSRFToken', csrf_token);

    var data = JSON.parse('{}');
    data['follow'] = isFollowRequest;
    data['target_user_id'] = current_user_id;
    data['isFollow'] = isFollowRequest;

    setFollowXHR.setRequestHeader("Content-Type", "application/json");

    setFollowXHR.send(JSON.stringify(data));

    changeFollowUI(!isFollowRequest, false);
}

function changeFollowUI (isFollowButton, isOwner) {

    if (isOwner) {
        ownerMsg.style.display = 'block';
        return;
    }

    if (isFollowButton) {
        unfollowBtn.style.display = 'none';
        followBtn.style.display = 'block';
    } else {
        followBtn.style.display = 'none';
        unfollowBtn.style.display = 'block';
    }
} 
followStatusXHR.onload = function () {
    // hide spinner + change ui
    followSpinner.style.display = 'none';

    console.log(followStatusXHR.responseText);

    try {
        response = JSON.parse(followStatusXHR.responseText);

        if (response['isOwner'] == true) {
            changeFollowUI(true, true);
            return;
        } else {
            changeFollowUI(!response['hasUserFollowed'], false);

        }
    } catch (e) {
        console.log(e);
    }

    

}