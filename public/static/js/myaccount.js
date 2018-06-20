var answer;

testSuccessRe = new RegExp("Success!")

function confirmTransaction(id) {
    var request = "/conftrans?transid=" + id;

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
    var request = "/canctrans?transid=" + id;

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
    var request = "/cancprod?prodid=" + id;

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
        document.getElementById("product_status_" + id).innerHTML = "ended";
    }

    alert(answer);
}

function cancelReport(id) {
    var request = "/cancrep?repid=" + id;

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
        document.getElementById("report" + id).innerHTML = "";
    }

    alert(answer);
}

