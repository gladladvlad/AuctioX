window.onload = function(){

    inputUsername = document.getElementById("inputUsername")
    inputPassword = document.getElementById("inputPassword")

    signInButton = document.getElementById("signInButton")

    console.log("Onload() finished.")
}

function signIn(){

    data = {}
    data["username"] = inputUsername.value;
    data["password"] = inputPassword.value;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {

        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            console.log(xhr.responseText)
            return;
        }
    }

    xhr.open("POST", "/signinrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));
}
