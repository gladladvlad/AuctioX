window.onload = function(){
    console.log("onload() finished");
}

function request(){
    var request = "/signinrequest/?user=" + user + "&pass=" + pass;
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            alert(xhr.responseText);
        }
    }

    xhr.open("GET", request, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();
}

