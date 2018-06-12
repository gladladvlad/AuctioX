window.onload = function(){

    inputUsername==document.getElementById("inputEmail")
    inputPassword==document.getElementById("inputPassword")

    signInButton == document.getElementById("signInButton");

    signInButton.onclick = signIn();

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
            //body = document.getElementsByTagName("body")[0].innerHTML = xhr.response;
            alert(xhr.response);
            return;
        }
    }

    xhr.open("POST", "/signIn", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(data);
}
