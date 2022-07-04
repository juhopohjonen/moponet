
/*
get like status (has user liked)
via api (xmlhttprequest post)
*/

var likeStatus = null;

var likeRequest = new XMLHttpRequest();
likeRequest.open('POST', likeStatusApiUrl);

likeRequest.addEventListener('load', gotCallBack);

// add cors token in headers
// to prevent CORS (token defined
// in template )

likeRequest.setRequestHeader(
    'X-CSRFToken',
    csrftoken
)

likeRequest.send();

// function for parsing content reveived
// in callback
function gotCallBack () {
    var rawText = likeRequest.responseText;
    try {
        // make sure that the request
        // and the response are valid.

        if (likeRequest.status != 200 && JSON.parse(likeRequest.responseText['hasUserLiked'] != null)) {
            throw "error";
        }
    } catch (e) {
        alert('Virhe tykkäystietoja ladattaessa. Virhekoodi ' + likeRequest.status.toString());
    }

    // update like button (call manageLikeButtonStatus)

    var hasUserLiked = JSON.parse(likeRequest.responseText)['hasUserLiked'];
    manageLikeButtonStatus(hasUserLiked);

} 

function manageLikeButtonStatus (like) {
    var likeButton = document.getElementById('likeButton');
    var disLikeButton = document.getElementById('disLikeButton');

    // hide spinner
    document.getElementById('likeSpinner').style.display = 'none';

    // if user has liked, show dislike button
    // if user hasn't, then show like button. 

    if (like) {
        likeButton.style.display = 'none';
        disLikeButton.style.display = 'block';
    } else {
        likeButton.style.display = 'block';
        disLikeButton.style.display = 'none';
    }
}


/* if addLike argument == true
then add like, if false then
remove like. */
function like (addLike) {
    manageLikeButtonStatus(addLike)

    likeStatus = addLike.toString();
    // generate url + TRY to send likeXHR
    
    var urlWithArgs = likeApiUrl + '?like=' + addLike.toString();

    try {
        var likeXHR = new XMLHttpRequest();
        likeXHR.open('POST', urlWithArgs);
        likeXHR.addEventListener('load', gotLikeResp);

        likeXHR.setRequestHeader('X-CSRFToken',
        csrftoken
        )

        likeXHR.onerror = function () {

            toastAlert('Tykkäys epäonnistui <i class="fa-solid fa-thumbs-down"></i>',
            'Yhteydessä palvelimeen on jotain häikkää, jonka takia tykkääminen epäonnistui. <i class="fa-solid fa-thumbs-down"></i>');
            manageLikeButtonStatus(true);
            
        };

        likeXHR.send();


    } catch (e) {
        console.log(e);
        toastAlert('Tykkäys epäonnistui <i class="fa-solid fa-thumbs-down"></i>',
        'Yhteydessä palvelimeen on jotain häikkää, jonka takia tykkäys epäonnistui. <i class="fa-solid fa-thumbs-down"></i>');
        manageLikeButtonStatus(true);
    }
}

function gotLikeResp() {

    // notify user in case of error.

    addLike = likeStatus;
    if (addLike == 1 && this.status == 200) {
        toastAlert('Tykkäsit moposta! <i class="fa-solid fa-thumbs-up"></i>',
        'Tykkäsit moposta onnistuneesti. <i class="fa-solid fa-thumbs-up"></i>')
    } else if (addLike == 0 && this.status == 200) 
    {
        toastAlert('Poistit tykkäyksen <i class="fa-solid fa-thumbs-down"></i>',
        'Tykkäys poistettiin onnistuneesti. <i class="fa-solid fa-thumbs-down"></i>')
    }
}

function toastAlert(title, content) {
    var alertContent = content;
    // Built-in function
    halfmoon.initStickyAlert({
      content: alertContent,      // Required, main content of the alert, type: string (can contain HTML)
      title: title     // Optional, title of the alert, default: "", type: string
    })

  }

