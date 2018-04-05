window.onload = function(){

    signInButton == document.getElementById("signInButton");

    signInButton.onclick = SignIn;

    console.log("Onload() finished.")
}

function SignIn(){
    inputUser = document.getElementById("inputEmail");
    inputPass = document.getElementById("inputPassword");

    user = inputUser.value;
    pass = inputPass.value;

    console.log(user + ' ' + pass);

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