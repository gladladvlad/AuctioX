var answer;

testSuccessRe = new RegExp("Success!")

function confirmTransaction(id) {
    var request = "/conftrans?prodid=" + id;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            answer = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();

    alert(answer);
}

function cancelTransaction(id) {
    var request = "/canctrans?prodid=" + id;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            answer = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();

    if (testSuccessRe.test(answer)) {
        document.getElementById("transaction" + id).innerHTML = "";
    }

    alert(answer);
}

function cancelBid(id) {
    var request = "/cancbid?bidid=" + id;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            answer = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();

    if (testSuccessRe.test(answer)) {
        document.getElementById("bid" + id).innerHTML = "";
    }

    alert(answer);
}

function cancelProduct(id) {
    var request = "/cancprod?bidid=" + id;

    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200){
            answer = xhr.responseText;
        }
    }

    xhr.open("GET", request, false);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send();

    if (testSuccessRe.test(answer)) {
        document.getElementById("product" + id).innerHTML = "";
    }

    alert(answer);
}
