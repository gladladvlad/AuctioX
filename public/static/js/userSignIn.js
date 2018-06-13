window.onload = function(){

    inputUsername = document.getElementById("inputUsername")
    inputPassword = document.getElementById("inputPassword")

    errorField = document.getElementById("errors")

    signInButton = document.getElementById("signInButton")

    console.log("Onload() finished.")
}

function signIn(){

    data = {}
    data["username"] = inputUsername.value;
    data["password"] = inputPassword.value;

    errorField.innerHTML = ""

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {

        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            console.log(xhr.responseText)
            response = JSON.parse(xhr.responseText)
            errorList = response["errors"]
            for(i = 0; i < errorList.length; i++) {
                errorField.innerHTML += " " + errorList[i]
                if(i < errorList.length - 1) {
                    errorField.innerHTML += "<br>"
                }
            }

            if(response["success"])
            {
                window.location = "/"
            }

            return
        }
    }

    xhr.open("POST", "/signinrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log(JSON.stringify(data))
    xhr.send(JSON.stringify(data));
}
