function sendUserRegisterRequest() {
    console.log("sendUserRegisterRequest()")

    inputEmail = document.getElementById("inputEmail");
    inputUsername = document.getElementById("inputUsername");
    inputPassword = document.getElementById("inputPassword");
    inputConfirmPassword = document.getElementById("inputConfirmPassword");

    inputCountry = document.getElementById("inputCountry");
    inputState = document.getElementById("inputState");
    inputCity = document.getElementById("inputCity");
    inputAddress1 = document.getElementById("inputAddress1");
    inputAddress2 = document.getElementById("inputAddress2");
    inputZipCode = document.getElementById("inputZipCode");

    inputName = document.getElementById("inputName");
    inputTel = document.getElementById("inputTel");

    data = {}

    data['email'] = inputEmail.value
    data['username'] = inputUsername.value
    data['password'] = inputPassword.value
    data['confirmPassword'] = inputConfirmPassword.value
    data['country'] = inputCountry.value
    data['state'] = inputState.value
    data['city'] = inputCity.value
    data['address1'] = inputAddress1.value
    data['address2'] = inputAddress2.value
    data['zipCode'] = inputZipCode.value
    data['name'] = inputName.value
    data['tel'] = inputTel.value

    form = new FormData()

    errorField = document.getElementById("errors")
    errorField.innerHTML = ""

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            console.log(xhr.responseText)
            return
            response = JSON.parse(xhr.responseText)
            for(er in response["errors"]) {
                errorField.innerHTML += er + "<br>"
            }
            console.log(response["success"])
            return
        }
    }

    xhr.open("POST", "/registrationrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));
}