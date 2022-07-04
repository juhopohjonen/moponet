

function signUpUser() {
    // cornfirm password 

    pwd = document.getElementById('password').value;


    if (pwd != document.getElementById('passconfirm').value) {
        error(
            "Syötä valitsemasi salasana 'Salasana' -kenttään ja kirjoita sama salasana 'Vahvista salasana' -kenttään.",
            'Salasanat eivät täsmää',
            document.getElementsByClassName('container')[0]
            )
        return;
    }

    

    // create xhr, set listener

    var request = new XMLHttpRequest();
    request.addEventListener('load', listenResponse);

    // create data object, add user form data into it.

    data_obj = JSON.parse('{}')

    data_obj["username"] = document.getElementById('username').value;
    data_obj["email"] = document.getElementById('email').value;
    data_obj["password"] = document.getElementById('password').value;

    // open, add csrf_token + send request

    request.open('POST', request_url);
    request.setRequestHeader('X-CSRFToken', csrf_token);

    request.send(JSON.stringify(data_obj));
    
}

function listenResponse() {
    
    // try to parse the response, catch => set resp_obj null

    try {
        resp_obj = JSON.parse(this.responseText);
    } catch
    {
        resp_obj = null;
    }

    // this function is called when the server has responded.
    // check for errors, show message if exists, otherwise show default message (func error)

    if (this.status != 200 && resp_obj != null && resp_obj["message"] != null) {

        error(resp_obj["message"]);
        return;

    } else if (this.status != 200) {

        error();
        return;
    }

    // success :) redirect to redirect_url ( if not null )

    var redirect_url = resp_obj["redirect_url"];

    if (redirect_url != null) {

        setTimeout(() => {
            window.location.replace(redirect_url);
        }, 2000);
        
        success(message="Käyttäjän luonti onnistui. Olet nyt kirjautunut sisään!");
    }
}


// show error message
function success (message="Jotain tapahtui oikein!", title="Onnistui!", container=document.getElementsByClassName('container')[0]) {
    // remove all existing success alerts (.alert)
    
    for (var i = 0; i < document.getElementsByClassName('alert').length; i++) {
        document.getElementsByClassName('alert')[i].remove();
    }

    // create new err msg+contents and append errorMsg to base

    var errorMessage = document.createElement('div')
    errorMessage.classList = 'alert alert-success suc-msg mt-10';
    errorMessage.role = 'alert';


    var msgHeading = document.createElement('h4');
    msgHeading.innerHTML = title;

    errorMessage.appendChild(msgHeading);
    errorMessage.append(message);

    // insert error message before first heading (as first node)
    var firstElem = container.childNodes[1];

    container.insertBefore(errorMessage, firstElem);
}



function error (message="Jotain tapahtui, pahoittelemme tilannetta.", title="Virhe", container=document.getElementsByClassName('container')[0]) {
    // remove all existing alerts
    
    for (var i = 0; i < document.getElementsByClassName('alert').length; i++) {
        document.getElementsByClassName('alert')[i].remove();
    }

    // create new err msg+contents and append errorMsg to base

    var errorMessage = document.createElement('div')
    errorMessage.classList = 'alert alert-danger err-msg mt-10';
    errorMessage.role = 'alert';


    var msgHeading = document.createElement('h4');
    msgHeading.innerHTML = title;

    errorMessage.appendChild(msgHeading);
    errorMessage.append(message);

    // insert error message before first heading (as first node)
    var firstElem = container.childNodes[1];

    container.insertBefore(errorMessage, firstElem);
}
