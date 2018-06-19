window.onload = function(){

    inputQuestion = document.getElementById('questionBox')
    errorField = document.getElementById("errors")
}


function ToggleAnswerBox(boxId) {
    box = document.getElementById(boxId)
    if (box.style.display == 'flex') {
        box.style.display = 'none'
    }
    else {
        box.style.display = 'flex'
    }
}

function sendQuestionRequest(prodId){

    data = {}
    data["text"] = inputQuestion.value;
    data["productId"] = prodId;

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
                location.reload();
            }

            return
        }
    }

    xhr.open("POST", "/postquestionrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log(JSON.stringify(data))
    xhr.send(JSON.stringify(data));
}


function sendAnswerRequest(answerKey, prodId){

    data = {}
    data["text"] = document.getElementById("text_" + answerKey).value
    data["productId"] = prodId;
    data["answerKey"] = answerKey;

    answerErrors = document.getElementById("errors_" + answerKey)

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
                location.reload();
            }

            return
        }
    }

    xhr.open("POST", "/postanswerrequest", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log(JSON.stringify(data))
    xhr.send(JSON.stringify(data));
}