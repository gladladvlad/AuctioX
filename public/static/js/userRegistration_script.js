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

    inputFirstName = document.getElementById("inputFirstName");
    inputLastName = document.getElementById("inputLastName");
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
    data['firstName'] = inputFirstName.value
    data['lastName'] = inputLastName.value
    data['tel'] = inputTel.value

    errorField = document.getElementById("errors")
    errorField.innerHTML = ""

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            response = JSON.parse(xhr.responseText)
            errorList = response["errorList"]
            for(i = 0; i < errorList.length; i++) {
                errorField.innerHTML += " " + errorList[i]
                if(i < errorList.length - 1) {
                    errorField.innerHTML += "<br>"
                }
            }

            if(response["success"])
            {
                alert("Registration successful!")
                window.location = "/"
            }

            return
        }
    }

    xhr.open("POST", "/registrationrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));
}